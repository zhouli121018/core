<template>
    <section class="m-layout">
        <div class="u-lmask j-layout-loading" style="display: none;">
            <div class="u-lmask-floater"></div>
            <div class="u-lmask-content"><div class="u-lmask-loading"></div></div>
        </div>

        <aside class="lysidebar j-layout-nav">
            <div class="icon j-switch-mainpage"  title="主页" @click="jumpTo('/mailbox')"><i class="iconfont icon-iconhome"></i></div>
            <div class="avatar">
                <a href="javascript:void(0);" class="u-img u-img-round">
                    <img class="j-avatar" alt="avatar" src="@/assets/img/man.png">
                </a>
            </div>
            <div class="divider"></div>
            <div class="j-wrapper">

                    <div class="icon" :class="{active:activeTab==t.id}" v-for="t in tabs" :key="t.id" title="t.title" @click="changeTab(t.id)">
                        <i class="iconfont" :class="t.iconclass"></i>
                    </div>

                    <div role="toLunkr" class="icon j-lunkr lunkr" title="论客">
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
                        <li><a href="#" class="skin-primary-hover-color" @click.prevent.stop="lockscreen">锁屏</a></li>
                        <li><a href="#" class="skin-primary-hover-color" @click="logout">退出</a></li>
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
import store from '@/store'
import router from '@/router'
import cookie from '@/assets/js/cookie';
export default {
    data:function(){
        return {
            activeTab:0,
            tabs:[
                {id:0,title:'我的邮箱',iconclass:'icon-youxiang'},
                {id:1,title:'我的日程',iconclass:'icon-iconschedule'},
                {id:2,title:'文件中心',iconclass:'icon-iconfiler'},
                {id:3,title:'联系人',iconclass:'icon-iconcontacts'},
                {id:4,title:'应用中心',iconclass:'icon-iconmore'},
            ]
        }
    },
    methods:{
        jumpTo(path){
            router.push(path)
        },
        changeTab(index){
            this.activeTab = index;
            if(index == 0){
                this.jumpTo('/mailbox')
            }else if(index == 1){
                this.jumpTo('/calendar')
            }
        },
        logout(){
            cookie.delCookie('token')
            cookie.delCookie('name')
            this.$store.dispatch('setInfo');
            router.push('/login')
        },
        lockscreen() {
            this.$confirm('<h3>您的邮箱将进入锁定状态</h3><p>邮箱将仍然保持在线</p><p>在输入正确的“邮箱密码”前任何人都无法动您的邮箱</p><p>可以更安全的保护您的隐私</p>', '锁屏提示', {
                dangerouslyUseHTMLString: true,
                distinguishCancelAndClose: true,
                confirmButtonText: '确定锁屏',
                cancelButtonText: '取消'
            })
            .then(() => {
                router.push('/lockscreen');
            })
            .catch(action => {
               
            });
        }

    }
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

