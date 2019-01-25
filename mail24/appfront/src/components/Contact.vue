<template>
  <div>
    <el-row :gutter="10" style="margin-bottom:10px;">
          <el-col :span="6" :offset="6">
            <el-input :placeholder="lan.SETTING_RE_ADD_CONTENT_RULE" v-model="contact_search" class="input-with-select" size="small">
              <el-button slot="append" icon="el-icon-search"  @click="search_dept"></el-button>
            </el-input>
          </el-col>
        </el-row>
    <el-row  :gutter="10">
      <el-col :span="6" >
        {{lan.SETTING_RE_ADD_SELECTDPT_PLACE}}：
      </el-col>
      <el-col :span="12">
        {{lan.CHOOSE_CONTACT_DESC}}：
      </el-col>
      <el-col :span="6">
        {{lan.CHOOSE_CONTACT_ALREADY}}：(<b>{{toList.length}}</b>)
      </el-col>

    </el-row>
    <el-row  :gutter="10">
      <el-col :span="6" >
        <div style="height:420px;overflow: auto;width:100%;border:1px solid #dcdfe6">
           <!--:default-expanded-keys="default_expanded"-->
            <!--:default-checked-keys="default_checked"-->
            <!--:expand-on-click-node="false"-->
          <el-tree
            :default-expanded-keys="[0]"
            node-key="id"
            :data="transform_menu"
            accordion
            ref="contactTreeRef"
            :highlight-current="true"
            :props="defaultPropsCon"
            @node-click="contact_tree_click">
            <span  slot-scope="{ node, data }" :title="node.label">
              <i v-if="data.children && data.children.length==0" class="iconfont icon-icongroup"></i>
              <span>{{ node.label }}</span>
            </span>
          </el-tree>
        </div>
      </el-col>
      <el-col :span="12" style="height:420px;border-left:2px dotted #dcdfe6;border-right:2px dotted #dcdfe6;">

        <el-table
          height="420"
          v-loading="loading"
          :data="contactData"
          tooltip-effect="dark"
          style="width: 100%"
          @row-click="rowClick" @selection-change="select_change"
          @select="selectionChange_contact" @select-all="selectionChange_contact"  ref="contactTable" :header-cell-style="{background:'#f0f1f3'}">
          <el-table-column
            type="selection"
            width="35">
          </el-table-column>
          <el-table-column prop="fullname" :label="lan.COMMON_XINGMING">
            <template slot-scope="scope">
              <i v-if="scope.row.is_dept" style="" :title="lan.COMMON_DEPARTMENT" class="iconfont icon-icongroup"></i>
              <i v-if="!scope.row.is_dept" style="color:#2976A8;" class="iconfont icon-icon-gender-man"></i>
              <span>{{ scope.row.fullname|| scope.row.name}}</span>
            </template>
          </el-table-column>
          <el-table-column  :label="lan.MAILBOX_COM_COMPOSE_MAIL_ADDRESS">
            <template slot-scope="scope">
              <span>{{scope.row.email || scope.row.pref_email || scope.row.username}}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="6" style="height:420px;">
        <div class="address_box" style="border: 1px solid #dcdfe6;
          height: 420px;
          overflow-y: auto;
          padding: 4px;
          -webkit-box-sizing: border-box;
          box-sizing: border-box;">
          <el-row v-for="(t,k) in toList" :key="k" class="hover_show_box">
            <el-col :span="22" style="overflow: hidden;white-space: nowrap" :title="t.username||t.email">{{t.name||t.fullname}}
              <span v-if="t.username">&lt;{{t.username||t.email}} &gt; </span>
            </el-col>
            <el-col :span="2" style="text-align: right">
              <i class="el-icon-error delete_hover" @click="deleteList('to',t.id,k)"></i>
            </el-col>
          </el-row>
        </div>
      </el-col>

    </el-row>
    <el-row :gutter="10" style="margin-bottom:10px;">
          <el-col :span="18" :offset="6">
            <el-pagination
              @size-change="handleSizeChange_contact"
              @current-change="handleCurrentChange_contact"
              :current-page="currentPage"
              :page-sizes="[10, 20,50,100]"
              :page-size="page_size_add"
              layout="total,prev, slot, next,sizes,jumper"
              v-if="totalCount>0"
              :total="totalCount">
              <span> {{currentPage+' / '+Math.ceil(totalCount/page_size_add)}}</span>
            </el-pagination>
          </el-col>
        </el-row>
  </div>
</template>
<script>
  import lan from '@/assets/js/lan';
  import { contactOabDepartsGet,contactOabMembersGet} from '@/api/api'
  export default {
    name:'Contact',
    data(){
      return {
        loading:false,
        contact_search:'',
        totalCount:0,
        oabchildren:[],
        contactSelection:[],
        toList:[],
        hashTo:[],
        contactData:[],
        currentPage:1,
        page_size_add:10,
        pid:0,
        transform_menu: [],
        defaultPropsCon: {
          id:'id',
          label: 'label',
          children: 'children',
        },
      }
    },
    methods: {
      search_dept(){
        this.currentPage = 1
        // this.oabchildren = [];
        this.getOabMembers();
      },
      handleSizeChange_contact(val){
        this.currentPage = 1
        this.page_size_add = val;
        this.getOabMembers();
      },
      handleCurrentChange_contact(val){
        this.currentPage = val
        this.getOabMembers();
      },
      deleteList(a,id,k){
        this.hashTo[id] = false;
        this.toList.splice(k,1)
        this.bang(this.toList)
      },
      bang(arr){
        if(this.$refs.contactTable)this.$refs.contactTable.clearSelection()
        for(let i=0;i<arr.length;i++){
          for(let k=0;k<this.contactData.length;k++){
            if(arr[i].id == this.contactData[k].id){
              this.$refs.contactTable.toggleRowSelection(this.contactData[k],true);
              break;
            }
          }
        }
      },
      select_change(selection){
        this.contactSelection = selection;
      },
      rowClick(row){
        this.$refs.contactTable.toggleRowSelection(row)
        this.selectionChange_contact(this.contactSelection,row);
      },
      selectionChange_contact(v,row){
        console.log(v) //selection
          if(!row){
            let rows = this.contactData;
            if(v.length>0){
              for(let key in rows){
                if(!this.hashTo[rows[key].id]){
                  this.hashTo[rows[key].id] = true;
                  this.toList.push(rows[key]);
                }
              }
            }else{
              for(let i=0;i<rows.length;i++){
                if(this.hashTo[rows[i].id]){
                  this.hashTo[rows[i].id] = false;
                  for(let j=0;j<this.toList.length;j++){
                    if(this.toList[j].id == rows[i].id){
                      this.toList.splice(j,1);
                      break;
                    }
                  }
                }
              }
            }
          }else{
            if(this.hashTo[row.id]){
              this.hashTo[row.id] = false;
              for(let i=0;i<this.toList.length;i++){
                if(row.id == this.toList[i].id){
                  this.toList.splice(i,1);
                  break;
                }
              }
            }else{
              this.hashTo[row.id] = true;
              this.toList.push(row);
            }
          }
      },
      getOabMembers() {
        this.loading = true;
        let keys = new Array();
        // keys.push(Number(this.oab_cid));
        // this.default_expanded_keys = keys;
        // this.default_checked_keys = keys;

        var param = {
          "page": this.currentPage,
          "page_size": this.page_size_add,
          "search": this.contact_search,
          "dept_id": this.pid,
        };
        contactOabMembersGet(param).then((res) => {
          this.loading = false;
          this.totalCount = res.data.count;
          this.contactData = res.data.results;
          this.contactData.forEach(val => {
            val.pid = this.pid;
          })
          if(this.currentPage == 1){
            this.contactData = this.oabchildren.concat(this.contactData)
          }
          setTimeout(() => {
            // this.bang(this.allSeclect)
          }, 50)
        }).catch(err=>{
          this.loading = false;

        });
      },
      contact_tree_click(data){
        let _this = this;
        console.log(data);
        this.pid = data.id;
        this.$refs.contactTreeRef.setCurrentNode(data);
        this.currentPage = 1;

        this.oabchildren = [];
        if(data.id>0){
          data.name = data.label;
          data.is_dept = true;
          this.oabchildren.push(data)
        }

        if(data.children.length>0){
            let paramArr = [];
            for(let i=0;i<data.children.length;i++){
              data.children[i].name = data.children[i].label;
              data.children[i].is_dept = true;
              paramArr.push(data.children[i]);
            }
            _this.oabchildren = _this.oabchildren.concat(paramArr);
            _this.getOabMembers();
          }else{
            this.getOabMembers();
          }
      },
      getDeptList(){
        contactOabDepartsGet().then(res=>{
          console.log(res)
          this.transform_menu = res.data.results;
        }).catch(err=>{
          console.log('获取部门列表错误！',err)
        })
      },
    },
    created(){
      this.getDeptList();
      if(this.contactData.length==0){
          this.getOabMembers();
        }
    },
    watch:{
      toList(newVal){
        this.$emit('getData', newVal);
      }
    },
    computed:{
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
    }
  }
</script>
<style scoped>
  .delete_hover{
    color:red;
    display:none;
    cursor:pointer;
  }
  .hover_show_box{
    padding:2px 0;
  }
  .hover_show_box:hover{
    background:rgb(240, 241, 243);
  }
  .hover_show_box:hover .delete_hover{
    display:inline-block;
  }
  .address_box{
    border:1px solid #dcdfe6;height:180px;margin-bottom:20px;overflow-y: auto;padding:4px;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }
  .address_box:hover,.address_box.active{
    border-color:#409EFF
  }
  .address_box.active{
    border-color:#409EFF;
    box-shadow: 0 0 5px #409eff;
  }
</style>
