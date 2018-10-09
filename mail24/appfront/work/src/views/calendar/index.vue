<template>
  <div>

    <section class="m-mail">

      <aside class="fl-g-sidebar">
        <div class="fl-m-nav-bg"></div>
        <ul class="fl-m-nav j-file-nav">
          <li>
            <a class="fl-m-nav-trigger" :class="{'fl-nav-current':selectedIndex == 0}"  href="#"  title="日程管理"  @click.prevent.stop="jumpTo('/calendar/set',{id:0})">
                <span>
                  <i class="menu_icon_box iconfont icon-iconsetschedule"></i>
                  <div>日程管理</div>
                </span>
            </a>
          </li>
          <li v-for="(c,k) in calendars" :key="c.id">
            <a class="fl-m-nav-trigger" :class="{'fl-nav-current':selectedIndex == c.id}" href="#"  :title="c.name" @click.prevent.stop="jumpTo('/calendar/index',c)">
                <span>
                  <i class="iconfont icon-iconmyschedule menu_icon_box"></i>
                  <div>{{c.name}}</div>
                </span>
            </a>
          </li>
          <li v-for="(c,k) in share_calendars" :key="c.calender_id">
            <a class="fl-m-nav-trigger" :class="{'fl-nav-current':selectedIndex == c.calender_id}" href="#"  :title="c.name" @click.prevent.stop="jumpTo('/calendar/index',c)">
                <span>
                  <i class="iconfont icon-iconmyschedule menu_icon_box"></i>
                  <div>{{c.name}}</div>
                </span>
            </a>
          </li>
        </ul>
      </aside>

      <article class="fl-g-content">
        <div class="cal-content-wrap">
          <router-view :calendar_id="calendar_id"></router-view>
          <!--<Calendar :calendar_id="calendar_id"></Calendar>-->
        </div>
      </article>

    </section>



  </div>
</template>
<script>
  import {contactOabDepartsGet,contactOabMembersGet,getCalendarsList} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    data() {
      return {
        selectedIndex:'1',
        calendar_id:'',
        calendars:[
          {id:1,mailbox_id:7368,name:'我的日程'},
          {id:2,mailbox_id:7368,name:'xx的日程'},
          ],
        share_calendars:[
          {id:6,mailbox_id:7368,name:'共享日程1'},
          {id:7,mailbox_id:7368,name:'共享日程2'},
          {id:8,mailbox_id:7368,name:'共享日程3'},
        ],
      };
    },
    components: {

    },
    created: function() {

    },
    mounted: function() {
      this.getCalendars();
      if(this.$route.path.indexOf('/calendar/set')>=0){

      }
    },
    methods: {
      jumpTo(path,c){
        this.$router.push(path);
        this.selectedIndex = c.calender_id||c.id;
        if(c.id&&c.id!=0){this.calendar_id = c.calender_id||c.id;}
      },
      getCalendars(){
        getCalendarsList().then(res=>{
          this.calendars = res.data.results;
          for(let i=0;i<res.data.results.length;i++){
            let o = res.data.results[i];
            if(o.is_default){
              this.calendar_id = o.id;
              if(this.$route.path.indexOf('/calendar/index')>=0){
                this.selectedIndex = o.id;
              }else{
                this.selectedIndex = 0;
              }
            }
          }
          this.share_calendars = [];
          for(let i=0;i<res.data.share_results.length;i++){
            let o = res.data.share_results[i];
            console.log(o.is_show)
            if(o.is_show){
              this.share_calendars.push(o)
            }
          }
        },err=>{
          console.log(err);
        })
      }

    },
    computed: {

    },

  }
</script>
<style>
  @import 'fullcalendar/dist/fullcalendar.css';

  .fc-day-grid-event .fc-content{
    text-overflow: ellipsis;
  }
  .fc-event{
    position:relative;
  }
  .fc-event-container>a:hover{
    background-color:#c9e9ff !important;
    border-color:#c9e9ff !important;
  }
  /*.fc-event-container:hover{*/
    /*background-color:#c9e9ff !important;*/
  /*}*/
  .fc-agendaWeek-view.fc-agenda-view{
    /*width:60%;*/
  }
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
    height: 100%;
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
  .fl-g-sidebar>ul{
    background:rgba(255,255,255,.6)
  }
</style>
