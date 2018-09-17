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
          <full-calendar :events="fcEvents" :config="config" @event-selected="eventClick" @day-click="dayClick"></full-calendar>
        </div>
      </article>

    </section>

  </div>
</template>
<script>
  export default {
    data() {
      return {

        config: {
          locale: "zh-cn",
          defaultView: 'month',
          editable: true,
          droppable: true,
          buttonText: {
            today: '今天',
            month:'月',
            agendaWeek:'周',
            agendaDay:'日',
            listMonth:'事件',
          },
          header:{
            right:  'month,agendaWeek,agendaDay,listMonth'
          }
        },
        fcEvents : [
          {
            title : '标记32测试测试吃测试吃测试测试测试测色测色测试',
            start : '2018-09-11 14:30:00',
            backgroundColor: 'red',
            borderColor: 'red',
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


    },
    created: function() {

    },
    mounted: function() {

    },
    methods: {
      jumpTo(path){
        this.$router.push(path);
      },
      dayClick (t){
        console.log(t.toLocaleString())
        // e.target.style.boxShadow="0 0 5px #60CAFF"

      },
      eventClick (data){
        console.log(arguments)
        alert(data.title)
      },
    },
    computed: {

    },

  }
</script>
<style>
  @import 'fullcalendar/dist/fullcalendar.css';
  .cal-content-wrap>div{
    background: rgba(255,255,255,.8);
  }
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
    padding: 8px;
    overflow-y:auto;
    box-sizing:border-box;
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
