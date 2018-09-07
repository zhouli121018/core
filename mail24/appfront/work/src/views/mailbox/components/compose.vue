<template>
    <div class="mltabview-content">
      <div class="mltabview-panel">
        <section class="m-mlcompose">
          <div class="toolbar" style="background:#fff;">
            <div id="pagination" class="f-fr">
                <div class="" @click="show_contact = !show_contact">
                    <el-button size="small">通讯录</el-button>
                </div>
            </div>

            <el-button size="small" type="primary">发送</el-button>
            <el-button-group >
              <el-button size="small" @click="preview">预览</el-button>
              <el-button size="small">存草稿</el-button>
            </el-button-group>

             <el-button  size="small" plain>
                取消
            </el-button>
          </div>


          <div class="main" ref="iframe_height">
            <div class="mn-aside right_menu" :class="{show_contact:show_contact}">
              <el-tabs v-model="activeName">
                <!--个人通讯录-->
                <el-tab-pane label="个人通讯录" name="first">
                  <el-input  placeholder="搜索" prefix-icon="el-icon-search" v-model="filterText">
                  </el-input>

                  <el-tree class="filter-tree" :data="contactList" :props="defaultProps" :filter-node-method="filterNode"
                   @node-click="selectContact"  accordion :indent="2" ref="tree2" v-loading="contact_loading">
                  </el-tree>
                </el-tab-pane>

                <!--信纸-->
                <el-tab-pane label="信纸" name="second">
                  <ul c>
                    <li><a href="#" @click="">
                      <img src="../img/none_zh.png" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#" class="active">
                      <img src="../img/Peace_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/Buckle_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/LeatherCowBoy_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/Lilium_martagan_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                    <li><a href="#">
                      <img src="../img/Lotus_m.jpg" alt="">
                      <span class="bg"></span>
                    </a></li>
                  </ul>
                </el-tab-pane>
                <el-tab-pane label="模板信" name="third">模板信</el-tab-pane>
              </el-tabs>
            </div>
            <form class="u-form mn-form"  :class="{right0:show_contact}">
              <div class="form-tt compose_title">
                <el-form size="mini" inline-message :model="ruleForm2" status-icon ref="ruleForm2" label-width="80px" class="demo-ruleForm" style="font-size:16px;">
                  <el-form-item label="发件人:">
                    <el-input type="text" value="myself@test.com" readonly auto-complete="off"></el-input>
                  </el-form-item>

                  <el-form-item label="收件人:" >
                    <div class="padding_15">
                        <div class="mailbox_s" :class="{error:!v.status}" v-for="(v,k) in maillist" :key="k" :title="v.mailbox"><b>{{ v.mailbox }}</b><i class="el-icon-close" @click="deleteMailboxForKey(k,v)"></i></div>
                        <el-autocomplete  class="no_padding"  v-model="state1" :fetch-suggestions="querySearch" @keydown.8.native="deleteMailbox"
                        @blur="addMailbox" @focus="insertMailbox=1" placeholder="" @select="handleSelect">

                          <!--<template slot-scope="{ item }" :trigger-on-focus="false">-->
                            <!--<div class="name" style="width:300px;">{{ item.value }}</div>-->
                          <!--</template>-->
                        </el-autocomplete>



                      <el-button class="" @click.native="transform_dialog = true" style="float:right;">选择收件人</el-button>
                    </div>

                  </el-form-item>
                  <el-form-item label="抄   送:" prop="copyer">
                    <div class="padding_15">
                      <div class="mailbox_s" :class="{error:!v.status}" v-for="(v,k) in maillist_copyer" :key="k" :title="v.mailbox"><b>{{v.mailbox}}</b><i class="el-icon-close" @click="deleteMailboxForKey_copyer(k,v)"></i></div>
                      <el-autocomplete  class="no_padding" v-model="state_copyer" :fetch-suggestions="querySearch" @keydown.8.native="deleteMailbox_copyer"
                        @blur="addMailbox_copyer" @focus="insertMailbox=2" placeholder=""  @select="handleSelect_copyer" ></el-autocomplete>
                    </div>
                  </el-form-item>
                  <el-form-item label="主  题:" prop="subject">
                    <el-input v-model="ruleForm2.subject"></el-input>
                  </el-form-item>
                  <el-form-item label="密  级:" prop="secret">
                    <el-input v-model.number="ruleForm2.secret" readonly></el-input>
                  </el-form-item>

                  <el-form-item v-show="fileList.length>0" label="附  件:" prop="attach">
                    <div  v-for="(f,k) in fileList" :key="f.id" class="attach_box" @mouseenter="attach_hoverfn(f.id)" @mouseleave="remove_attach_hover" :class="{attach_hover:attachIndex == f.id}">
                      <i class="el-icon-document"></i>
                      <span >[非密] {{f.filename}}</span>
                      <i class="el-icon-check" style="margin:0 5px;color:#26af1e;font-weight:bold;"></i>
                      <span class="plan_style">{{f.size | mailsize}}</span>
                      <span class="attach_actions">
                        <el-button size="mini" type="primary" plain @click="delete_attach(f.id,k)">删除</el-button>
                        <el-button size="mini" type="primary" plain>下载</el-button>
                        <el-button size="mini" type="primary" plain>预览</el-button>
                        <el-button size="mini" type="primary" plain>密级修改</el-button>
                      </span>
                    </div>
                  </el-form-item>
                  <el-upload
                      class="upload-demo"
                      action=""
                      :http-request="uploadFile"
                      :show-file-list="false"
                      multiple :on-progress="uploadProgress" :on-success="sucUpload">
                      <el-button size="small" type="primary" id="addAttachBtn"><i class="el-icon-upload"></i> 添加附件</el-button>
                      <div slot="tip" class="el-upload__tip"></div>
                  </el-upload>
                  <el-dropdown  placement="bottom" @command="selectUpload" style="margin-right:20px;">
                      <i class="el-icon-caret-bottom"></i>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item  command="filecore">从文件中心添加</el-dropdown-item>
                      <el-dropdown-item  command="upload">上传到文件中转站</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>

                  <el-dropdown trigger="click" placement="bottom-start">
                    <el-button type="primary" size="small">
                      签名<i class="el-icon-caret-bottom el-icon--right"></i>
                    </el-button>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item>不使用签名档</el-dropdown-item>
                      <el-dropdown-item divided>aaa</el-dropdown-item>
                      <el-dropdown-item>dadsaf</el-dropdown-item>
                      <el-dropdown-item divided>编辑签名档</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>

                  <el-upload
                      action=""
                      :http-request="imgChange"
                      :show-file-list="false"
                      multiple  style="display:inline-block;">
                      <el-button size="small" type="primary"> 插入图片</el-button>
                  </el-upload>

                </el-form>
              </div>
              <div class="form-edr compose_editor" ref="editor_box">

                <!--<div v-html="content"></div>-->

                <editor id="editor_id" ref="editor_id" height="400px" width="100%" :content="content"
                    :afterChange="afterChange"
                    pluginsPath="/static/kindeditor/plugins/"

                    :loadStyleMode="false" :items="toolbarItems" :uploadJson="uploadJson"
                    @on-content-change="onContentChange"  :autoHeightMode="false">

                </editor>

              </div>
              <div class="form-toolbar compose_footer">
                <div>
                  <el-checkbox v-model="number_sign">数字签名</el-checkbox>
                  <el-checkbox v-model="safe_secret">安全加密</el-checkbox>
                </div>
                <div class="bt-hd-wrap">
                  <el-checkbox v-model="number_sign">保存到"已发送"</el-checkbox>
                  <el-checkbox v-model="safe_secret">设为"紧急"</el-checkbox>
                  <el-checkbox v-model="number_sign">已读回执</el-checkbox>
                  <el-checkbox v-model="safe_secret">定时发送</el-checkbox>
                  <el-checkbox v-model="number_sign">阅后即焚</el-checkbox>
                  <el-checkbox v-model="safe_secret">邮件加密</el-checkbox>
                  <el-checkbox v-model="number_sign">禁止转发</el-checkbox>
                </div>
              </div>
            </form>
          </div>
        </section>
      </div>


      <el-dialog title="通讯录" :visible.sync="transform_dialog" :append-to-body="true" width="1032px">
        <el-row  :gutter="20">
          <el-col :span="6" >
            <el-tree

              show-checkbox
              :data="transform_menu"
              :props="defaultPropsCon">
            </el-tree>
          </el-col>
          <el-col :span="18" style="border-left:1px solid #dcdfe6;">
            <div>
              <el-transfer
                style="text-align: left; display: inline-block"
                v-model="value4"
                filterable
                :titles="['联系人', '选中联系人']"

                :format="{
                  noChecked: '${total}',
                  hasChecked: '${checked}/${total}'
                }"

                :data="transformData">
                <!--@change="handleChange"-->
                <span slot-scope="{ option }">{{ option.key }} - {{ option.label }}</span>
                <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button>
                <el-button class="transfer-footer" slot="right-footer" size="small">操作</el-button>
              </el-transfer>
            </div>
          </el-col>

        </el-row>
        <div slot="footer" class="dialog-footer" >
          <el-button @click="transform_dialog = false">取 消</el-button>
          <el-button type="primary" @click="transform_dialog = false">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="文件中心" :visible.sync="coreFileDialog" :modal-append-to-body="false">
        <el-pagination class="margin-bottom-5"
          @size-change="attachSizeChange"
          @current-change="attachCurrentChange"
          :current-page="attachCurrentPage"
          :page-sizes="[5,10,20,50,100, 200, 300, 400]"
          :page-size="attachPageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="attachTotal" small>
        </el-pagination>
        <el-table @selection-change="fileSelectionChange"
          ref="multipleTable" :data="coreFileList" tooltip-effect="dark" style="width: 100%"
          >
          <el-table-column type="selection"  width="55"></el-table-column>
          <el-table-column prop="filename" label="文件名" ></el-table-column>
          <el-table-column prop="size" label="文件大小" width="100" >
            <template slot-scope="scope">
                <span  class="plan_style">{{scope.row.size | mailsize}}</span>
            </template>
          </el-table-column>
        </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button @click="coreFileDialog = false" size="small">取 消</el-button>
          <el-button type="primary" @click="addAttachfn" size="small">确 定</el-button>
        </div>
      </el-dialog>
    </div>

</template>
<script>
  import axios from 'axios';
  import { contactPabGroupsGet,contactPabMapsGet,contactPabMembersGet,postAttach,deleteAttach,getAttach,contactOabDepartsGet } from '@/api/api'

  export default {
    props:{
      iframe_height:'',
    },

    data(){
      const generateData = _ => {
        const data = [];
        for (let i = 1; i <= 15; i++) {
          data.push({
            key: i,
            label: `备选项 ${ i }`,
            disabled: false
          });
        }
        console.log(data)
        return data;
      };
      return {
        contact_loading:false,

        transform_menu: [{
          id: 1,
          label: '个人通讯录',
          children: []
        }, {
          id: 2,
          label: '组织通讯录',
          children: [{
            id: 5,
            label: '二级 2-1'
          }, {
            id: 6,
            label: '二级 2-2'
          }]
        }, {
          id: 3,
          label: '公共通讯录',
          children: [{
            id: 7,
            label: '二级 3-1'
          }, {
            id: 8,
            label: '二级 3-2'
          }]
        }, {
          id: 4,
          label: '其它域通讯录',

        }],
        defaultPropsCon: {
          id:'id',
          label: 'label',
          children: 'children',
        },
        transformData: generateData(),
        value4: [],
        extraFileUploadParams : {
                        csrfmiddlewaretoken:this.$store.state.userInfo.token,
                         id:123
                },
        afterChange:function (val) {
          console.log(val)
        },
        afterUpload:function(){
          console.log('afterupload')
        },
        afterSelectFile:function(){
          console.log('afterselect')
        },
        attachCurrentPage:1,
        attachPageSize:10,
        attachTotal:0,
        coreFileList:[

        ],
        hashFile:[],
        fileSelection:[],
        coreFileDialog:false,
        show_contact:false,
        attachIndex:'',
        fileList: [],
        imgSrc:'',
        transform_dialog:false,
        filterText:'',
        hashMail:[],
        insertMailbox:1,
        hashMail_copyer:[],
        maillist:[

        ],
        maillist_copyer:[],
        restaurants:[

        ],
        state1:'',
        state_copyer:'',
        toolbarItems:
        ['source', '|','formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
        'italic', 'underline',  'lineheight', '|',  'justifyleft', 'justifycenter', 'justifyright',
        'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', '|','subscript',
        'superscript', 'link', 'unlink','image',  'table','hr','|', 'undo', 'redo', 'preview',
           'fullscreen',
         ],
        content:'<div>内容</div>',
        activeName: 'first',
        number_sign:false,
        safe_secret:true,
        ruleForm2: {
          reciver: [],
          copyer: '',
          subject: '',
          secret:'非密'
        },
        contactList: [
          {
          id: 1,
          label: 'aaa组',
          children: [{
            id: 4,
            label: 'yc@test.com',
          }]},
          {
          id: 2,
          label: '未分组联系人',
          children: [{
            id: 5,
            label: 'lw@test.com'
          }, {
            id: 6,
            label: 'system@domain.com'
          }]},

          ],
        defaultProps: {
          children: 'children',
          label: 'label'
        }

      };
    },
    methods:{
      get_transform_menu(){
        let arr = [];
        let _this = this;
        contactPabGroupsGet().then(res=>{
          arr.push()
        })
        axios.all([contactPabGroupsGet(),contactOabDepartsGet()]).then(axios.spread(function (acct, perms) {
          // 两个请求现在都执行完成
          let cc =
          arr[0] = {
            id:'pab',
            label:'个人通讯录',
            children:acct.data.pab_contact_groups
          }
          arr[1] = {
            id:'oab',
            label:'组织通讯录',
            children:perms.data.results
          }
          _this.transform_menu = arr;

        }))
      },
      handleChange(value, direction, movedKeys) {
        console.log(value, direction, movedKeys);
      },
      sizeFormatter(row,col){
        return (row.size/1024).toFixed(2) +' KB';
      },
      attachSizeChange(val){
        this.attachPageSize = val;
        this.getAttachList();
      },
      attachCurrentChange(val){
        this.attachCurrentPage = val;
        this.getAttachList();
      },

      addAttachfn(){
        for(let i=0;i<this.fileSelection.length;i++){
          if(!(this.hashFile[this.fileSelection[i].id])){
            this.hashFile[this.fileSelection[i].id] = true
            this.fileList.push(this.fileSelection[i]);
          }
        }
        this.coreFileDialog = false;
        this.fileSelection = [];
      },
      fileSelectionChange(val) {
        this.fileSelection = val;
        console.log(this.fileSelection)
      },
      selectUpload(command){
        if(command == 'filecore'){
          this.coreFileDialog = true;
        }else if(command == 'upload'){
          document.getElementById('addAttachBtn').click()
        }
      },
      getAttachList(){
        let param={
          limit:this.attachPageSize,
          offset:(this.attachCurrentPage-1)*this.attachPageSize
        };
        getAttach(param).then((suc)=>{
          console.log(suc.data)
          this.attachTotal = suc.data.count;
          this.coreFileList = suc.data.results;
        },(err)=>{
          console.log(err);
        })
      },
      delete_attach(id,k){
        deleteAttach(id).then((suc)=>{
          console.log(suc);
          this.hashFile[this.fileList[k].id]=false;
          this.fileList.splice(k,1);
        },(err)=>{
          console.log(err);
        })
      },
      attach_hoverfn(key){
        this.attachIndex = key;
      },
      remove_attach_hover(){
        this.attachIndex = '';
      },
      uploadFile(param){
        var file = param.file;
        var formData=new FormData();
        formData.append('filepath', file)
        postAttach(formData).then((res)=>{
          console.log(res.data)
          var obj = res.data;
          this.hashFile[res.data.id]=true;
          this.fileList.push(res.data)
          console.log(this.fileList)
         this.$message({
             message:"上传成功",
             type:'success'
         })
        },(err)=>{
          this.$message({
               message:"上传失败",
               type:'error'
          })
        })
        return true;
      },
      uploadProgress(event, file, fileList){
        console.log("ev")
        console.log(event)
        console.log("fi")
        console.log(file)
        console.log('jl')
        console.log(fileList)
      },
      sucUpload(response, file, fileList){
        console.log('res')
        console.log(response)
        console.log('file')
        console.log(file)
        this.fileList.push(file);
        console.log('filelist')
        console.log(fileList)
      },
      imgChange(param){
        console.log(this.$store.state.userInfo.token)
        var file= param.file;
        // this.imageFileName.push(file.name);
            const isJPG = file.type === 'image/jpeg';
            const isGIF = file.type === 'image/gif';
            const isPNG = file.type === 'image/png';
            const isBMP = file.type === 'image/bmp';
            const isLt2M = file.size / 1024 / 1024 < 10;

            if (!isJPG && !isGIF && !isPNG && !isBMP) {
                this.$alert('上传图片必须是JPG/GIF/PNG/BMP 格式!', '提示：', {
                  confirmButtonText: '确定'
                });
                return;
            }
            if (!isLt2M) {
                this.$alert('上传图片大小不能超过 10MB!', '提示：', {
                  confirmButtonText: '确定'
                });
                return;
            }

        var _this = this;
        console.log(param)
        // var o = document.getElementById('img_upload');

        var reader=new FileReader();
        reader.readAsDataURL(file);
        reader.onload=function (e) {//上传成功，执行上传成功之后的事件
        var str=e.target.result;
        //将上传成功后的图片显示在特定位置
        this.imgSrc = str;
        console.log(_this.$refs.editor_id)
          _this.$refs.editor_id.editor.insertHtml(`<img src=${str} />`)


        }
      },
      onContentChange (val) {
        this.content = this.$refs.editor_id.$data.outContent;
      },

      preview(){
        //ke-toolbar-icon ke-toolbar-icon-url ke-icon-preview
        let btn = document.querySelector('.ke-toolbar-icon.ke-toolbar-icon-url.ke-icon-preview');
        btn.click();
      },
      addMailbox(){
        setTimeout(()=>{this.handleSelect()},300)
      },
      deleteMailbox(){
        if(!this.state1&&this.maillist.length>0){
          this.hashMail[this.maillist[this.maillist.length-1].mailbox] = false;
          this.maillist.pop();
        }
      },
      deleteMailboxForKey(k,v){
        this.hashMail[v.mailbox] = false;
        this.maillist.splice(k,1)
      },
      handleSelect(item) {
        // console.log(item);
        if(this.state1){
          if(this.hashMail[this.state1]){

          }else{
            this.hashMail[this.state1] = true;
            let obj = {};
            obj.mailbox = this.state1;
            obj.status = true;
            this.maillist.push(obj);
            this.state1 = '';
          }
        }
        this.state1 = '';
      },
      addMailbox_copyer(){
        setTimeout(()=>{this.handleSelect_copyer()},300)
      },
      deleteMailbox_copyer(){
        if(!this.state_copyer&&this.maillist_copyer.length>0){
          this.hashMail_copyer[this.maillist_copyer[this.maillist_copyer.length-1].mailbox] = false;
          this.maillist_copyer.pop();
        }
      },
      deleteMailboxForKey_copyer(k,v){
        this.hashMail_copyer[v.mailbox] = false;
        this.maillist_copyer.splice(k,1)
      },
      handleSelect_copyer(item) {
        // console.log(item);
        if(this.state_copyer){
          if(this.hashMail_copyer[this.state_copyer]){

          }else{
            this.hashMail_copyer[this.state_copyer] = true;
            let obj = {};
            obj.mailbox = this.state_copyer;
            obj.status = true;
            this.maillist_copyer.push(obj);
            this.state_copyer = '';
          }
        }
        this.state_copyer = '';
      },
      querySearch(queryString, cb) {
        var restaurants = this.restaurants;
        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) >= 0);
        };
      },
      loadAll() {
        return [
          { "value": "anna<Anna@test.com>" },
          { "value": "李威<lw@test.com>" },
          { "value": "系统<system@domain.com>"  },
        ];
      },
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      selectContact(data){
        if(!data.children){
          if(this.insertMailbox==1){
          if(!this.hashMail[data.label]){
            this.hashMail[data.label]=true;
            this.maillist.push({mailbox:data.label,status:true});
          }
        }else if(this.insertMailbox == 2){
          if(!this.hashMail_copyer[data.label]){
            this.hashMail_copyer[data.label]=true;
            this.maillist_copyer.push({mailbox:data.label,status:true});
          }

        }
        }

      },
      //获取个人通讯录组数据
      getPabGroups(){
        let _this = this;
        let param = {
          "group_id":0,
          "page_size":10000,
          "page":1
        }
        contactPabMembersGet(param).then((suc)=>{
          let arr = [];
          for(let i=0;i<suc.data.results.length;i++){
            let o = suc.data.results[i];
            let obj = {};
            obj.id = o.contact_id;
            let str = o.fullname + '<'+o.email+'>';
            obj.value = str;
            arr.push(obj);
          }
          this.restaurants = arr;
        },(err)=>{
          console.log(err);
        })

        contactPabGroupsGet().then(res=>{
          this.contact_loading = true;
          let resultArr = [];
          let total = res.data.results[res.data.results.length-1].count;
          let axiosArr = [];
          for(let i=0;i<res.data.pab_contact_groups.length;i++){
            let ob = res.data.pab_contact_groups[i];
            let param = {
              "page": 1,
              "page_size":total,
              "search": '',
              "group_id": ob.id,
              "is_group": 1,
            };
            axiosArr.push(contactPabMapsGet(param))
            resultArr.push({label:ob.label,id:ob.id,children:[]})
          }
          axiosArr.push(contactPabMembersGet({"page":1,"page_size":total,"group_id":0,"is_group":0,"search":''}))
          resultArr.push({label:'未分组联系人',id:0,children:[]})

          axios.all(axiosArr).then(axios.spread(function () {
            // 所有请求现在都执行完成
            for(let k = 0;k<arguments.length;k++){
              let ko = arguments[k];
              resultArr[k]['label'] += ' （'+ko.data.count+'）'
              for(let j=0;j<ko.data.results.length;j++){
                let obj = {};
                obj.id = ko.data.results[j].contact_id;
                obj.email = ko.data.results[j].email;
                obj.fullname = ko.data.results[j].fullname;
                obj.label = ko.data.results[j].fullname + '<'+ko.data.results[j].email+'>';
                resultArr[k]['children'].push(obj)
              }
            }
            _this.contactList = resultArr
            _this.contact_loading = false;
          }))
        })
      },

    },
    mounted() {
      // this.restaurants = this.loadAll();
      this.getPabGroups();
      this.getAttachList();
      this.get_transform_menu();
    },
    computed:{
      uploadJson:function(){
        return this.$store.state.uploadJson;
      }
    },
    watch: {
      filterText(val) {
        this.$refs.tree2.filter(val);
      }
    },

  }
</script>
<style>
  .margin-bottom-5{
    margin-bottom:5px;
  }
  .show_contact{
    opacity: 0;
    filter: alpha(opacity=0);
  }
  .m-mlcompose .mn-form.right0{
    right:0;

  }
  .m-mlcompose .upload-demo{
    display:inline-block;
  }
  .attach_actions{
    display:none;
  }
  .attach_hover .attach_actions{
    display:inline-block;
  }
  .attach_box .el-button--mini{
    border:none;
    color:#409EFF;
    padding: 7px 10px;
  }
  .right_menu .el-tabs__nav-scroll{
    padding-left:10px;
  }
  .right_menu .el-tabs__content{
    padding:0 10px;
  }
  .mn-aside.right_menu{
    padding:0;
    width:240px;
    box-sizing:border-box;
  }
  .right_menu ul li{
    width:50%;
    float:left;
    text-align:center;
    margin-bottom:20px;
  }
  .right_menu ul li a{
    border:1px solid #e3e4e5;
    display:inline-block;
    position:relative;
    width: 78px;
    height: 48px;

  }
  .right_menu ul li a.active{
    border:1px solid transparent;
  }
  .right_menu ul li a.active .bg{
    background: url(../img/selected.gif) no-repeat;
    width: 80px;
    height: 52px;
    display: block;
    position: absolute;
    z-index: 9;
    top: 0;
    left: 0;
  }
  .compose_title input{
    border:none;
    /*border-bottom:1px solid #dcdfe6;*/
    border-radius:0;
  }
  .compose_title .el-form-item{
    border-bottom:1px solid #dcdfe6;
    margin-bottom:6px;
  }
  .compose_title .el-select{
    width:100%;
  }
  .compose_title .el-input--mini{
    font-size:15px;
  }
  .compose_footer>div{
    padding:0 14px;
  }
  .m-mlcompose .mn-form .form-edr.compose_editor{
    /*position:absolute;*/
    /*top:224px;*/
    /*bottom:72px;*/
    /*height:auto;*/
  }
  .compose_editor [data-name="preview"]{
    display:none;
  }
  .mailbox_s{
    float:left;white-space:nowrap;
    cursor:pointer;
    border:1px solid #a3d9d2;
    background-color: #e4f7f5;
    margin-right:6px;
    padding:0 4px;
    border-radius:12px;
  }
  .mailbox_s.error{
    background-color: #f2dede;
    border-color: #ebccd1;
    color: #a94442;
  }
  .mailbox_s>b{
    margin-right:4px;
  }
  .compose_title .no_padding .el-input__inner{
    padding:0;
  }
  .padding_15{
    padding-left:15px;
  }
</style>

