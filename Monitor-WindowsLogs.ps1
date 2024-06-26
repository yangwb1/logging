# PowerShell 脚本：Monitor-WindowsLogs.ps1

# 配置 RabbitMQ 连接参数
$hostname = "localhost"
$port = 5672
$username = "guest"
$password = "guest"
$exchange = "logs"
$routingKey = "log"

# 添加 RabbitMQ.Client.dll 引用
Add-Type -Path "D:\BaiduNetdiskWorkspace\code\python-flask-logging\RabbitMQ.Client.dll"

# 使用完全限定名来避免 CLS 兼容性问题
$factory = New-Object RabbitMQ.Client.ConnectionFactory
$factory.HostName = $hostname
$factory.UserName = $username
$factory.Password = $password
$connection = $factory.CreateConnection()
$channel = $connection.CreateModel()
$channel.ExchangeDeclare($exchange, [RabbitMQ.Client.ExchangeType]::Direct, $true)

# 定义日志监控
$logName = "Application"
$log = New-Object System.Diagnostics.EventLog
$log.Log = $logName

# 事件处理函数
$onEntryWritten = {
    param($sender, $e)

    $logMessage = @{
        LogName = $e.Entry.LogName
        TimeGenerated = $e.Entry.TimeGenerated
        EntryType = $e.Entry.EntryType
        Source = $e.Entry.Source
        Message = $e.Entry.Message
    } | ConvertTo-Json

    $body = [System.Text.Encoding]::UTF8.GetBytes($logMessage)
    $channel.BasicPublish($exchange, $routingKey, $null, $body)
    Write-Host "Sent: $logMessage"
}

# 订阅日志事件
$log.EnableRaisingEvents = $true
Register-ObjectEvent -InputObject $log -EventName "EntryWritten" -Action $onEntryWritten

# 保持脚本运行
Write-Host "Monitoring $logName logs..."
while ($true) {
    Start-Sleep -Seconds 10
}
