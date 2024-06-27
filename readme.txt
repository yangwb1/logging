日志分析系统
项目架构图
Winlogbeat --> Logstash --> RabbitMQ --> Python (数据处理和消费)
                                 |
                                 V
                               Elasticsearch --> Python (数据处理和消费)
                                 |
                                 V
                               Kibana (数据可视化)


作者杨文兵
1、经常需要到服务器后台查日志，每次查看日志都需要申请服务器的权限。
2、于是想到，是否可以在页面上直接查看各个机房的配置文件。
3、设计一个页面，页面上可以查看各个节点的ip，以及对应的服务，查询日志还是查看配置文件。
4、

cd 到logstash根目录
 .\logstash -f "D:\Program Files\logstash-8.14.1\config\logstash.conf"

需要用管理员身份运行
 C:\Program Files\Elastic\Beats\8.14.1\winlogbeat
 .\winlogbeat.exe -e -c .\winlogbeat.yml


es启动
进入es的bin目录下
 .\elasticsearch.bat

#修改es密码
bin/elasticsearch-reset-password -u elastic


部署消息队列，订阅更新各个服务器的配置文件信息。
方法五是通过事件驱动的方式来实现配置更新和展示，具体步骤如下：

### 步骤一：部署事件总线或消息队列

1. **选择合适的事件总线或消息队列**：
   - 部署一个事件总线或消息队列，例如 RabbitMQ、Apache Kafka 等。这些工具可以用来发布和订阅事件，确保事件的可靠传递和处理。

### 步骤二：监听配置更新事件

1. **部署监听程序**：
   - 在每个集群节点上部署一个监听程序，该程序负责订阅配置更新事件。这个监听程序可以是一个独立的服务或进程，也可以集成到现有的应用中。

2. **订阅配置更新事件**：
   - 监听程序通过事件总线或消息队列订阅配置更新事件。配置更新事件可以包含更新的配置内容或配置文件的版本信息。

### 步骤三：更新本地配置

1. **获取更新并更新本地配置文件**：
   - 当配置更新事件发生时，监听程序会接收到事件通知。程序根据事件中的信息，例如配置文件的路径或版本号，从配置管理系统或存储中获取最新的配置内容。

2. **更新本地配置文件**：
   - 监听程序将获取到的最新配置内容更新到本地配置文件中。这可以是直接覆盖旧配置文件或者按需更新特定部分。

### 步骤四：Web页面实时展示

1. **使用WebSocket或长轮询技术**：
   - 在Web页面中，使用WebSocket或长轮询等实时通信技术，与集群中的监听程序建立连接。

2. **订阅配置更新通知**：
   - Web页面通过WebSocket或长轮询向监听程序订阅配置更新通知。当配置更新事件发生时，监听程序向所有订阅者发送更新通知。

3. **动态展示更新后的配置**：
   - 收到配置更新通知后，Web页面获取最新的配置信息，并动态展示到用户界面上。这样用户可以实时看到配置的变化和更新。

### 示例流程

- 假设集群中的某个节点更新了配置文件，例如数据库连接配置或应用程序设置。
- 监听程序在收到配置更新事件后，根据事件内容获取最新的配置信息。
- 监听程序将更新后的配置信息写入本地配置文件。
- Web页面通过WebSocket或长轮询实时获取更新的配置信息，并在页面上动态展示给用户。

### 注意事项

- **安全性**：确保事件传输和配置更新过程中的安全性，可以使用加密通信和身份验证机制。
- **性能和扩展性**：考虑消息队列或事件总线的性能特性和扩展能力，以应对高并发和大规模集群的配置管理需求。
- **故障处理**：实现容错机制，处理配置更新失败或网络中断等异常情况。

通过事件驱动的配置更新方法，可以实现集群配置的实时管理和动态展示，为复杂应用环境下的配置管理提供了一种有效的解决方案。


代码执行：python app.py


如果你选择使用 RabbitMQ（RMQ）作为消息队列来实现配置更新事件的订阅和处理，可以通过以下步骤部署监听程序：

### 部署监听程序步骤：

#### 1. 准备环境

在部署监听程序之前，确保你的环境中已经安装了以下软件和工具：

- Python 环境：确保你的目标服务器或容器中安装了 Python，并且具备运行你的监听程序所需的 Python 版本和依赖项。
- RabbitMQ 服务器：确保 RabbitMQ 服务器已经正确安装和配置，并且可以被监听程序访问。

#### 2. 编写监听程序

编写一个 Python 程序，用于连接 RabbitMQ，订阅配置更新的消息，并处理这些消息。下面是一个简单的示例代码：

```python
import pika  # 导入 RabbitMQ 的 Python 客户端库

# RabbitMQ 服务器的连接参数
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# 连接 RabbitMQ 服务器
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明一个名为 config_updates 的队列
channel.queue_declare(queue='config_updates')

# 定义接收消息的回调函数
def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

# 告诉 RabbitMQ 使用 callback 函数接收来自 config_updates 队列的消息
channel.basic_consume(queue='config_updates', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')

# 开始监听消息
channel.start_consuming()
```

#### 3. 部署监听程序

将编写好的 Python 程序部署到你的目标服务器或容器中：

- 将上述代码保存为一个 Python 脚本，例如 `config_listener.py`。
- 将脚本上传到目标服务器或容器中，确保 Python 环境和 RabbitMQ 客户端库 `pika` 已经安装。

#### 4. 启动监听程序

使用命令行或脚本在目标服务器或容器中启动监听程序：

```bash
python config_listener.py
```

#### 5. 测试和监控

- 测试监听程序：发送一个测试消息到 RabbitMQ 的 `config_updates` 队列，观察监听程序是否成功接收并处理消息。
- 监控运行状态：使用 RabbitMQ 的管理界面或其他监控工具，监视队列消息的情况和监听程序的运行状态。

### 注意事项

- **连接参数安全性**：确保在实际生产环境中使用安全的连接参数，例如使用 TLS/SSL 连接或者更复杂的认证方式。
- **错误处理**：在实际部署中，实现适当的错误处理和日志记录，以便追踪和解决可能出现的问题。
- **性能和扩展**：考虑如何处理大量的配置更新消息和高并发情况，以及如何扩展监听程序到多个节点来实现高可用性和负载均衡。

通过以上步骤，你可以成功部署一个基于 RabbitMQ 的监听程序，用来订阅和处理配置更新事件。这样可以在集群环境中实现配置的实时更新和管理。



