/** 基础信息 */
const Database = {
    /* 签到 */
    is_qiandao: true,
    /* 签到 */
    db_qiandao: false,
    /* 观看视频 */
    is_guankan: true,
    /* 一键三连 */
    is_sanlian: true,
    /* 发布文章 */
    is_wenzhang: false,
    /* 电子书打分 */
    is_dianzishu: true,
    accounts: [
        {
            name: 'wenxinxin',
            password: 'wxx123456'
        },
    ],
    /* 是否启用远程服务获取文章主题，选择否后需要手动填写主题(theme) */
    is_connect: false,
    IP: 'http://192.168.1.37:8000/',
    theme: '大规模数据处理框架 Hadoop 的概念与实践',
    /* 一次并发启动多少个账号，取决电脑性能 */
    max_run: 3,
    /** 签到完成后，等待系统缓冲时间(用于一键领取积分) */
    buffer_sleep: 50,
    /** 是否开启浏览器UI界面显示 */
    is_show: true,
    /** 日志信息 */
    Logging: {
        /** 日志存储位置 */
        log_file: 'C:\wz\work\app\python\ailiyun.log',
    }
}

module.exports = {
    Database
}