<template>
  <div>
    <full-calendar :events="fcEvents" ref="calendar" :config="config"
                         @event-selected="eventClick"
                         @day-click="dayClick"
                         @event-created="eventCreated"

          ></full-calendar>
  </div>
</template>
<script>
  import {contactOabDepartsGet,contactOabMembersGet,getCalendarsList} from '@/api/api'
  const emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  export default {
    data() {
      return {
        config: {
          height : window.innerHeight-120,

          eventColor:"#fff",
          eventTextColor:"#474545",
          locale: "zh-cn",
          defaultView: 'month',
          editable: true,
          droppable: true,
          selectable: true,
          diableResizing:true,
          // columnFormat:'周dd',
          titleFormat:'YYYY年MM月',
          buttonText: {
            today: '今天',
            month:'月',
            agendaWeek:'周',
            agendaDay:'日',
            listMonth:'事件',
          },
          header:{
            center:"prev title next",
            left:"today",
            right:  'month,agendaWeek,agendaDay,listMonth,timelineDay'
          },
          views:{
            agendaWeek: {
              titleFormat:'YYYY年MM月D日',
            },
            agendaDay:{
              titleFormat:'YYYY年MM月D日',
            }
          },
          eventMouseover: function (event, jsEvent, view) {
            console.log('in');
            $(jsEvent.currentTarget).attr('title',event.title)
          },
          eventMouseout: function (event, jsEvent, view) {
          },
          windowResize: function(view) {
              $('#calendar').fullCalendar('option', 'height', window.innerHeight-120);
          },
        },
        fcEvents : [
          {
            id:0,
            title:"新建事件...",
            start:'',
            color: '#EDF8FB',
            textColor:'#aaa'
          },
          {
            id:1,
            title : '标记32测试测试吃测试吃测试测试测试测色测色测试',
            start : '2018-09-11',
            end : '2018-9-13',
            allDay:true,
            // url:'http://www.baidu.com'
            // backgroundColor: 'red',
            // borderColor: 'red',
          },
          {
            id:2,
            title : '试测试测色你哦士大夫hi上的i和迫使对方屁哦士大夫横批哦撒旦测色测试',
            start : '2018-09-13 14:30:00',
            allDay:false,
            backgroundColor: 'red',
            borderColor: 'red'
          },
          {
            id:3,
            title : '标记2',
            start : '2018-09-20',
            end : '2018-09-20'
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
      dayClick (t){
        console.log(t.toLocaleString())
        // e.target.style.boxShadow="0 0 5px #60CAFF"
        // this.$refs.calendar.fireMethod('changeView', 'agendaDay')
        console.log(arguments)
        this.fcEvents[0].start=t;
      },
      eventClick (data){
        this.$parent.getDeptOptions();
        this.$parent.searchOabMembers(1);
        console.log(arguments)
        if(!data.id){
          // this.newForm.start_day
          this.$parent.newEventDialog = true;

        }else{
          console.log(data.start._i)
          if(data.end)console.log(data.end._i)
          this.$parent.viewForm.title = data.title
          this.$parent.viewForm.start_day = data.start
          this.$parent.viewForm.end_day = data.end
          this.$parent.viewForm.is_allday = data.allDay
          this.$parent.viewEventDialog = true;
        }

      },
      eventCreated(){
      },
    },
    computed: {

    },

  }
</script>
