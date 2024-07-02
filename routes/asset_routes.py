from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, Asset, AssetForm  # 使用绝对导入


bp = Blueprint('asset_routes', __name__)

# @bp.route('/', methods=['GET'])
# def list_assets():
#     assets = Asset.query.all()
#     return render_template('asset_list.html', assets=assets)

@bp.route('/<int:asset_id>/edit', methods=['GET', 'POST'])
def edit_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    form = AssetForm(obj=asset)

    if form.validate_on_submit():
        form.populate_obj(asset)
        db.session.commit()
        flash('Asset updated successfully.', 'success')
        return redirect(url_for('asset_routes.list_assets'))

    return render_template('asset_form.html', form=form, asset=asset)

@bp.route('/new', methods=['GET', 'POST'])
def new_asset():
    form = AssetForm()

    if form.validate_on_submit():
        asset = Asset()
        form.populate_obj(asset)
        db.session.add(asset)
        db.session.commit()
        flash('Asset created successfully.', 'success')
        return redirect(url_for('asset_routes.list_assets'))

    return render_template('asset_form.html', form=form, asset=None)

@bp.route('/<int:asset_id>/logs', methods=['GET'])
def view_asset_logs(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    # 获取资产相关的日志，可以根据需要调整获取日志的逻辑
    keyword = asset.ip_address
    date = request.args.get('date', '')
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    page = int(request.args.get('page', 1))

    if not log_file_exists():
        return "Log file not found", 404

    matched_lines = get_log_lines(keyword, date, '', start_time, end_time)
    paginated_lines, total_pages = paginate_logs_by_size(matched_lines, page)

    cleaned_lines = [line.strip() for line in paginated_lines]

    return render_template('view_asset_logs.html',
                           asset=asset,
                           log_content=cleaned_lines,
                           current_page=page,
                           total_pages=total_pages,
                           date=date,
                           start_time=start_time,
                           end_time=end_time)
