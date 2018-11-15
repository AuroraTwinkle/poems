# A poems project
#### user接口

- 修改资料:接口'/alterOrGetProfile',post方法,需要user_mail,user_name,user_avatar三个参数，返回{"status": , "message": ""}
- 获取资料:分两步，第一步，获取用户信息，接口'/alterOrGetProfile?user_mail=***'，返回{"user_name": "青莲居士", "user_avatar": "C:\\古诗词\\用户头像\\7ec2c530-e892-11e8-b935-6807158c25e3TIM图片20180915143941.png", "status": true}，第二步，接口'/getAvatar?user_avatar=',参数值为第一步得到的user_avatar的值，返回头像图片


