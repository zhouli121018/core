<template>
  <div>
    <section class="m-mail">
      <aside class="fl-g-sidebar">
        <div class="fl-m-nav-bg"></div>
        <ul class="fl-m-nav j-file-nav">
          <li>
            <a class="fl-m-nav-trigger" :class="{'fl-nav-current':activeT=='pfile'}" href="#" :title="plang.FILE_INDEX_P"  @click.prevent.stop="jumpTo('pfile')">
                <span>
                  <i class="menu_icon_box iconfont icon-iconmyfile"></i>
                  <div>{{plang.FILE_INDEX_P}}</div>
                </span>
            </a>
          </li>
          <li>
            <a class="fl-m-nav-trigger" href="#" :class="{'fl-nav-current':activeT=='cfile'}" :title="plang.FILE_INDEX_C" @click.prevent.stop="jumpTo('cfile')">
                <span>
                  <i class="iconfont icon-iconcompanyfile menu_icon_box"></i>
                  <div>{{plang.FILE_INDEX_C}}</div>
                </span>
            </a>
          </li>
          <li>
            <a class="fl-m-nav-trigger" href="#" :class="{'fl-nav-current':activeT=='afile'}" :title="plang.FILE_INDEX_A" @click.prevent.stop="jumpTo('afile')">
                <span>
                  <i class="iconfont icon-iconaccfile menu_icon_box"></i>
                  <div>{{plang.FILE_INDEX_A}}</div>
                </span>
            </a>
          </li>
        </ul>
      </aside>
      <article class="fl-g-content">
        <router-view @sendMail_net="sendMail_net"></router-view>
      </article>
    </section>
  </div>
</template>
<script>
  import lan from '@/assets/js/lan';
  import {getOpenoffice} from '@/api/api'
  export default {
    data() {
      return {
        pfileImage: "./img/pfile.jpg",
        activeT:'pfile'
      };
    },
    components: {
    },
    created: function() {
    },
    computed: {
      plang(){
        if(this.$store.getters.getLanguage=='zh-hans'){
          return lan.zh
        }else if(this.$store.getters.getLanguage=='zh-tw'){
          return lan.zh_tw
        }else if(this.$store.getters.getLanguage=='en'){
          return lan.en
        }else if(this.$store.getters.getLanguage=='es'){
          return lan.zh
        }else{
          return lan.zh
        }
      },
    },
    mounted: function() {
      if(this.$route.path=='/file/afile'){
        this.activeT='afile';
      }else if(this.$route.path=='/file/cfile'){
        this.activeT='cfile';
      }else if(this.$route.path=='/file/pfile'){
        this.activeT='pfile';
      }
    },
    methods: {
      jumpTo(path){
        this.activeT = path;
        this.$router.push('/file/'+path);
      },
      preview(a,type,cfid){
        console.log(a)
        if((a.file_size && a.file_size>10*1024*1024) || (a.size && a.size>10*1024*1024)){
          this.$message({
            type:'error',
            duration:6000,
            showClose:true,
            message: this.plang.FILE_INDEX_MSG1
          })
          return;
        }
        let size = a.size||a.file_size;
        let suffix,name;
        if(a.name){
          suffix = a.name.slice(a.name.lastIndexOf('.')+1)
          name = a.name
        }else{
          suffix = a.filename.slice(a.filename.lastIndexOf('.')+1)
          name = a.filename;
        }

        let href = window.location.origin+'/#/preview/?id='+a.id+'&type='+type+'&size='+ size+'&suffix='+suffix+'&name='+encodeURIComponent(name)+'&cfid='+cfid;
        console.log(href)
        window.open(href)
        return;
        let ww = window.open();
        let param = {
          type:type,
          id:a.id,
        };
        getOpenoffice(param).then(res=>{
          let href = '';
          if(res.data.is_openoffice){
            href = res.data.preview_url + encodeURIComponent(window.location.origin + res.data.source_url)
          }else{
            href = window.location.origin + res.data.source_url
          }
          ww.location = href
        }).catch(err=>{
          let str = '';
          if(err.non_field_errors){
            str = err.non_field_errors[0]
          }
          ww.document.body.innerHTML="<h4>"+this.plang.FILE_INDEX_MSG3+str+'</h4>';
        })
      },
      sendMail_net(row,sels,type){
        if(this.$store.getters.getSharedStatus.shareuser_all || this.$store.getters.getSharedStatus.shareuser_post ||this.$store.getters.getSharedStatus.shareuser_send){

        }else{
          this.$message({
            type:'error',
            message: this.plang.MAILBOX_SHARE_POWER
          })
          return
        }
        let _this = this;
        if(row == 'more'){
          let check = true;
          let arr = [];
          sels.forEach(val => {
            if(val.nettype == 'folder'){
              this.$message({
                type:'error',
                message: this.plang.FILE_INDEX_MSG2
              })
              check = false
              return;
            }
            let obj = {};
            obj.id = val.id;
            if(val.name){
              obj.name = val.name;
              obj.file_size = val.file_size;
            }else{
              obj.filename = val.filename;
              obj.size = val.size;
            }
            if(type=='company'){
              obj.is_company = true
            }
            arr.push(obj);
          })
          if(!check)return;
          this.$store.dispatch('setPfileNet',arr)
          this.$store.dispatch('setFileJ',true)
          this.$router.push('/mailbox/innerbox/INBOX')
        }else{
          let obj = {
            id:row.id
          }
          if(row.name){
            obj.name = row.name
            obj.file_size = row.file_size
          }else{
            obj.filename = row.filename
            obj.size = row.size
          }
          if(type=='company'){
            obj.is_company = true
          }
          let arr = [];
          arr.push(obj)
          this.$store.dispatch('setPfileNet',arr)
          this.$store.dispatch('setFileJ',true)
          this.$router.push('/mailbox/innerbox/INBOX')
        }
      },
    },
  }
</script>
<style>
  .content.content-list.height100{
    overflow-y:auto;
    overflow-x:hidden;
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
  .wrapper.u-scroll.top0{
    top:0
  }
  .mlmain.mltabview.overflow_auto{
    overflow-y: auto;
    overflow-x:hidden;
  }
  .clear:after{
    content:"";
    display:block;
    clear:both;
  }
  .m-mllist-row .el-form-item{
    margin:0px 0px 14px 0px;
  }
  .m-mllist-row .el-form{
    border-bottom:1px solid #d4d7d9;
  }

  .el-form--inline .el-form-item {
    display: inline-block;
    margin-right: 0px;
    vertical-align: top;
  }
  .el-breadcrumb {
    font-size: 13px;
    line-height: 1;
  }
  .height100{
    height:100%;
  }
</style>
