<template>
  <div id="calendar_id" ref="calendar">

    <section class="m-mail" v-loading="listLoading">

      <aside class="fl-g-sidebar">
        <div class="fl-m-nav-bg"></div>
        <ul class="fl-m-nav j-file-nav">
          <li>
            <a class="fl-m-nav-trigger" :class="{'fl-nav-current':selectedIndex == 0}"  href="#"  :title="lan.CALENDAR_INDEX_CAL_MANAGER"  @click.prevent.stop="jumpTo('/calendar/set',{id:0})">
                <span>
                  <i class="menu_icon_box iconfont icon-iconsetschedule"></i>
                  <div>{{lan.CALENDAR_INDEX_CAL_MANAGER}}</div>
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
  import lan from '@/assets/js/lan';
  import {contactOabDepartsGet,contactOabMembersGet,getCalendarsList} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    data() {
      return {
        listLoading:false,
        selectedIndex:'1',
        calendar_id:'',
        calendars:[

          ],
        share_calendars:[

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
        this.listLoading = true;
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
            if(o.is_show){
              this.share_calendars.push(o)
            }
          }
          this.listLoading = false;
        }).catch(()=>{
          this.listLoading = false;
        })
      }

    },
    computed: {
      lan:function(){
        let lang = lan.zh
        if(this.$store.getters.getLanguage=='zh-hans'){
          lang = lan.zh
        }else if(this.$store.getters.getLanguage=='zh-tw'){
          lang = lan.zh_tw
        }else if(this.$store.getters.getLanguage=='en'){
          lang = lan.en
        }else if(this.$store.getters.getLanguage=='es'){
          lang = lan.zh
        }else{
          lang = lan.zh
        }
        return lang
      }
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
  /*.fc-event-container>a:hover{*/
    /*background-color:#c9e9ff !important;*/
    /*border-color:#c9e9ff !important;*/
  /*}*/
  .fc-event-container>a{
    opacity: 0.85;
  }
  .fc-event-container>a:hover{
    opacity: 1;
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
  .menu_icon_box.iconfont{
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
    word-break: break-all;
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
  #calendar_id .fl-g-sidebar {
    position: relative;
    width: 100px;
    height: 100%;
    border-right: 1px solid #e3e4e5;
    text-align: center;
    overflow-y: auto;
    overflow-x: hidden;
  }
  .fl-g-sidebar>ul{
    background:rgba(255,255,255,.6)
  }
</style>
