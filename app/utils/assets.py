from flask_assets import Bundle

bundles = {
    'app_js': Bundle(
        'js/app.js',
        filters='jsmin',
        output='dist/js/app.js.min'
    ),
    'app_css': Bundle(
        'styles/app.less',
        filters='less,cssmin',
        output='dist/styles/app.min.css'
    )
}
