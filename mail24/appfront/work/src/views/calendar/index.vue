<template>
  <div>

    <section class="m-mail">

      <aside class="fl-g-sidebar">
        <div class="fl-m-nav-bg"></div>
        <ul class="fl-m-nav j-file-nav">
          <li>
            <a class="fl-m-nav-trigger"  href="#"  title="日程管理"  @click.prevent.stop="jumpTo('/setting/user')">
                <span>
                  <i class="menu_icon_box el-icon-goods"></i>
                  <div>日程管理</div>
                </span>
            </a>
          </li>
          <li>
            <a class="fl-m-nav-trigger fl-nav-current" href="#"  title="我的日程" @click.prevent.stop="jumpTo('/calendar/index')">
                <span>
                  <i class="el-icon-sort menu_icon_box"></i>
                  <div>我的日程</div>
                </span>
            </a>
          </li>
        </ul>
      </aside>

      <article class="fl-g-content">
        <div class="cal-content-wrap">
          <full-calendar lang="zh" ref="calendar" defaultView="basicWeek" :options="config" :events="fcEvents"  @changeMonth="changeMonth" @dayClick="dayClick" @eventClick="eventClick" @moreClick="moreClick">

            <template slot="fc-body-card">
              <div  class="more-events">
                <p>modsfo</p>
                <p>modsfojosdf</p>
              </div>

            </template>
            <template slot="fc-header-right" >

              <el-button>123</el-button>
            </template>
          </full-calendar>
        </div>
      </article>

    </section>

  </div>
</template>
<script>
  export default {
    data() {
      return {

        config:{
          lang: 'en',
          weekends: false
        },
        fcEvents : [
          {
            title : '标记32测试测试吃测试吃测试测试测试测色测色测试',
            start : '2018-09-11',
            backgroundColor: 'red',
            borderColor: 'red',
            className: 'done'
          },
          {
            title : '标记2',
            start : '2018-09-10',
            end : '2018-09-10',
          }
        ],

      };
    },
    components: {
      'full-calendar': require('vue-fullcalendar'),

    },
    created: function() {

    },
    mounted: function() {

    },
    methods: {
      changeView() {

      },
      jumpTo(path){
        this.$router.push(path);
      },
      changeMonth(){
        console.log('month')
      },
      dayClick (t,e){
        alert(t.toLocaleString())
        console.log(e.target)

        // e.target.style.boxShadow="0 0 5px #60CAFF"

      },
      eventClick (data,event,pos){
        console.log(arguments)
        document.getElementsByClassName('more-events')[1].style.display='block'
        document.getElementsByClassName('more-events')[1].style.left=pos.left+'px';
        document.getElementsByClassName('more-events')[1].style.top=pos.top+'px';
      },
      moreClick (day, events, jsEvent) {
        console.log('moreCLick', day, events, jsEvent)
      }

    },
    computed: {

    },

  }
</script>
<style>
  .more-events{
    display:none;
  }
  .events-day.today{
    box-shadow: 0 0 5px #60CAFF;
  }
  .events-day:hover{
    box-shadow: 0 0 5px #60CAFF;
  }
  .events-day:hover .day-number{
    /*color:#fff;*/
  }
  .comp-full-calendar{
    /*width:100%;*/
    max-width:100%;
  }
  .cal-content-wrap {
    position: relative;
    height: 100%;
    padding: 0 8px;
    overflow-y:auto;
}
  .menu_icon_box{
    /*width:48px;height:45px;background:#ddd;*/
    /*display:inline-block;*/
    font-size:30px;
    margin-bottom:8px;
  }
  .fl-g-content {
    position: absolute;
    left: 101px;
    right: 0;
    top: 0;
    bottom: 0;
}
  .fl-m-nav li:first-child a {
    border-top: none;
}

.fl-m-nav a {
    position: relative;
    display: block;
    height: 100px;
    width: 100px;
    border: 1px solid #e3e4e5;
    border-left: none;
    font-size: 0;
    text-decoration: none;
    overflow: hidden;
    -webkit-transition: 200ms background-color ease;
    transition: 200ms background-color ease;
    outline: none;
}
.fl-m-nav a>span {
    display: inline-block;
    vertical-align: middle;
    padding-top:20px;
    font-size: 12px;
    color: #555;
    word-break: normal;
}
.fl-m-nav a.fl-nav-current {
    border-color: #e3e4e5;
    border-right-color: #fff;

}
.fl-m-nav a.fl-nav-current>span{
  color: #3f86e1;
}
  .fl-m-nav-bg {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: #fff;
    opacity: .6;
    filter: alpha(opacity=60);
}
  .fl-g-sidebar {
    position: relative;
    width: 100px;
    height: 100%;
    border-right: 1px solid #e3e4e5;
    text-align: center;
  }
</style>
