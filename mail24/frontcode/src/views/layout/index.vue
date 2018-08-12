<template>
    <section class="m-layout">
        <div class="u-lmask j-layout-loading" style="display: none;">
            <div class="u-lmask-floater"></div>
            <div class="u-lmask-content"><div class="u-lmask-loading"></div></div>
        </div>

        <aside class="lysidebar j-layout-nav">
            <div class="icon j-switch-mainpage" data-i18n="common/nav_main" i18n-target="title" title="主页"><i class="iconfont iconhome"></i></div>
            <div class="avatar">
                <a href="javascript:void(0);" class="u-img u-img-round">
                    <img class="j-avatar" alt="avatar" src="/coremail/XT5/89517/style/img/man.png">
                </a>
            </div>
            <div class="divider"></div>
            <div class="j-wrapper">
                <div class="icon active" data-trigger="mail" data-i18n="main/appname_MBOX" i18n-target="title" title="我的邮箱">
                    <i class="iconfont iconemail"></i>
                </div>
                
                    <div class="icon" data-trigger="calendar" data-i18n="main/appname_MYCAL" i18n-target="title" title="我的日程">
                        <i class="iconfont iconschedule"></i>
                    </div>
                
                
                    <div class="icon" data-trigger="file" data-i18n="common/nav_file" i18n-target="title" title="文件中心">
                        <i class="iconfont iconfiler"></i>
                    </div>
                
                
                    <div class="icon" data-trigger="contact" data-i18n="common/nav_contact" i18n-target="title" title="联系人">
                        <i class="iconfont iconcontacts"></i>
                    </div>
                
                <div class="icon" data-trigger="appcenter" data-i18n="common/nav_appcenter" i18n-target="title" title="应用中心">
                    <i class="iconfont iconmore"></i>
                </div>
                <div role="toLunkr" class="icon j-lunkr lunkr" data-i18n="common/nav_lunkr" i18n-target="title" title="论客">
                    <i class="iconfont iconlunkrlogo"></i>
                    <span></span>
                </div>
            </div>
            <div class="icon icon-help j-to-helpcenter" data-i18n="common/nav_help" i18n-target="title" title="帮助中心">
                <i class="iconfont iconhelp"></i>
            </div>
            <div class="icon icon-bottom" data-trigger="setting" role="toggle" data-i18n="common/nav_setting" i18n-target="title" title="设置">
                <i class="iconfont iconsetupcenter"></i>
            </div>
        </aside>

        <article class="lymain">
            <section>
                <header class="lyheader">
                    <div class="logo">
                        <a href="javascript:void(0);" class="u-img j-lylogo" data-trigger="mail.welcome">
                            <img src="@/assets/img/logo.png" alt="logo" style="width: 152px; height: 42px;">
                        </a>
                    </div>
                    <ul class="u-list u-list-horizontal">
                        <li id="qqLi"><a href="#">QQ咨询</a></li>
                        <li id="cloud">
                            <a target="_blank" href="https://cloud.icoremail.net/icmcenter/expCenter/showEvaXT5?userid=1qfUTJjqUn7UT7jmUntU7UjgUexUfJjmUntUa7jWUerUr7UAU1fUrJULUnrUTJjl" style="color:red;font-weight: bold;" data-target="title" data-i18n="main.CommentAward">评价赢大奖</a>
                        </li>
                        <li><a target="_blank" href="#" data-i18n="main.Webadmin">后台管理</a></li>
                        <li><a href="#" class="skin-primary-hover-color f-dn lunkr-bandage f-pr">移动端</a></li>
                        <li><a href="#" class="skin-primary-hover-color f-dn f-pr" >即时沟通</a></li>
                        <li><a href="#" class="skin-primary-hover-color f-dn j-migrate-mbox" >马上搬家</a></li>
                        <li><a href="#" class="skin-primary-hover-color" >锁屏</a></li>
                        <li><a href="#" class="skin-primary-hover-color">退出</a></li>
                        <li class="header-divider">
                            <a href="javascript:void(0);" class="skin-primary-hover-color history-notification-trigger j-history-notification-trigger unread">
                                <i class="iconfont icon-iconms"></i>
                            </a>
                        </li>
                        <li>
                            <div class="u-input-control">
                                <input type="text" class="u-input" id="lyfullsearch" maxlength="50" disabledhotkey="true"  placeholder="邮件全文搜索" autocomplete="off">
                                <span class="j-search u-search iconfont icon-iconsreachm"></span>
                            </div>
                        </li>
                    </ul>
                </header>
                <div class="lybg">
                    <div class="bg1"></div>
                    <div class="bg2"></div>
                    <div class="bg3"></div>
                    <div class="bg4"></div>
                    <div class="bg5"></div>
                </div>
                <div class="lycontent">
                    <router-view></router-view>
                </div>
            </section>
        </article>

    </section>
</template>

<script>
export default {
    
}
</script>

<style>
.lymain .lybg .bg3{
    background:url(../../assets/img/bg_bottom.jpg) repeat-x bottom;
    background-size: contain;
}
.lymain .lybg .bg4{
    background:url(../../assets/img/bg_left.jpg) no-repeat left bottom;
        background-size: contain;
}
.lymain .lybg .bg5{
    background:url(../../assets/img/bg_right.jpg) no-repeat right bottom;
    background-size: contain;
}
</style>

