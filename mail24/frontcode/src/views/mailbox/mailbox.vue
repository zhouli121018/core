<template>
    <div>
        <section class="m-mail">
            <aside class="mlsidebar">
                <div class="mlsidebar-bg"></div>
                <div class="u-btns">
                    <button class="u-btn u-btn-default u-btn-large btn-compose j-mlsb" type="button" data-op="compose"><i class="iconfont iconcreate"></i> <span class="title">写 信</span></button>
                    <button class="u-btn u-btn-default u-btn-large btn-inbox j-mlsb" type="button" data-op="inbox"><i class="iconfont iconinbox"></i></button>
                </div>

                <div class="wrapper u-scroll">
                    <ul class="ztree" id="mltree">
                        <li id="mltree_1" class="level0" @click="jumpTo('/layout1/mailbox/innerbox')" tabindex="0" hidefocus="true" ><a id="mltree_1_a" class="level0" treenode_a="" onclick="" target="_blank" style="" title="收件箱">
                            <span id="mltree_1_switch" title="" class="button level0 switch noline_docu" treenode_switch=""></span><span id="mltree_1_ico" title="" treenode_ico="" class="button ico_docu" style="width:0px;height:0px;"></span><span id="mltree_1_span" fid="1" style="width: 80%;"><div class="cnt">收件箱</div></span></a>
                            </li>
                            <li id="mltree_2"  class="level0" tabindex="0" hidefocus="true" treenode=""><a id="mltree_2_a" class="level0" treenode_a="" onclick="" target="_blank" style="" title="待办邮件"><span id="mltree_2_switch" title="" class="button level0 switch noline_docu" treenode_switch=""></span><span id="mltree_2_ico" title="" treenode_ico="" class="button ico_docu" style="width:0px;height:0px;"></span><span id="mltree_2_span" fid="-5" style="width: 80%;"><div class="cnt">待办邮件</div></span></a></li>

                            <li id="mltree_3" class="level0" tabindex="0" hidefocus="true" treenode=""><a id="mltree_3_a" class="level0" treenode_a="" onclick="" target="_blank" style="" title="草稿箱"><span id="mltree_3_switch" title="" class="button level0 switch noline_docu" treenode_switch=""></span><span id="mltree_3_ico" title="" treenode_ico="" class="button ico_docu" style="width:0px;height:0px;"></span><span id="mltree_3_span" fid="2" style="width: 80%;"><div class="cnt">草稿箱</div></span></a></li>

                            <li id="mltree_4" @click="jumpTo('/layout1/mailbox/outbox')" class="level0" tabindex="0" hidefocus="true" treenode=""><a id="mltree_4_a" class="level0" treenode_a="" onclick="" target="_blank" style="" title="已发送"><span id="mltree_4_switch" title="" class="button level0 switch noline_docu" treenode_switch=""></span><span id="mltree_4_ico" title="" treenode_ico="" class="button ico_docu" style="width:0px;height:0px;"></span><span id="mltree_4_span" fid="3" style="width: 80%;"><div class="cnt">已发送</div></span></a></li>
                            
                            <li id="mltree_5" class="level0" tabindex="0" hidefocus="true" treenode="">
                                <a id="mltree_5_a" class="level0 curSelectedNode" treenode_a="" onclick="" target="_blank" style="" title="其他文件夹"><span id="mltree_5_switch" title="" class="button level0 switch noline_close" treenode_switch=""></span><span id="mltree_5_ico" title="" treenode_ico="" class="button ico_close" style="width:0px;height:0px;"></span><span id="mltree_5_span" fid="-4" style="width: 80%;">
                                <div class="cnt">其他文件夹</div><i class="j-setting iconfont iconset" title="管理" style="display: block;"></i><i class="j-add iconfont iconadd" title="添加" style="display: block;"></i></span></a>
                            <ul id="mltree_5_ul" class="level0 " style="display: none;"><li id="mltree_6" class="level1" tabindex="0" hidefocus="true" treenode=""><a id="mltree_6_a" class="level1" treenode_a="" onclick="" target="_blank" style="" title="已删除"><span style="display: inline-block;width:5px"></span><span id="mltree_6_switch" title="" class="button level1 switch noline_docu" treenode_switch=""></span><span id="mltree_6_ico" title="" treenode_ico="" class="button ico_docu" style="width:0px;height:0px;"></span><span id="mltree_6_span" fid="4" style="width: 77%;"><div class="cnt">已删除</div></span></a></li><li id="mltree_7" class="level1" tabindex="0" hidefocus="true" treenode=""><a id="mltree_7_a" class="level1" treenode_a="" onclick="" target="_blank" style="" title="垃圾邮件"><span style="display: inline-block;width:5px"></span><span id="mltree_7_switch" title="" class="button level1 switch noline_docu" treenode_switch=""></span><span id="mltree_7_ico" title="" treenode_ico="" class="button ico_docu" style="width:0px;height:0px;"></span><span id="mltree_7_span" fid="5" style="width: 77%;"><div class="cnt">垃圾邮件</div></span></a></li><li id="mltree_8" class="level1" tabindex="0" hidefocus="true" treenode=""><a id="mltree_8_a" class="level1" treenode_a="" onclick="" target="_blank" style="" title="病毒文件夹"><span style="display: inline-block;width:5px"></span><span id="mltree_8_switch" title="" class="button level1 switch noline_docu" treenode_switch=""></span><span id="mltree_8_ico" title="" treenode_ico="" class="button ico_docu" style="width:0px;height:0px;"></span><span id="mltree_8_span" fid="6" style="width: 77%;"><div class="cnt">病毒文件夹</div></span></a></li></ul></li></ul>
                </div>
            </aside>
            <router-view></router-view>
        </section>
    </div>
</template>
<script>
import router from '@/router'
export default {
    data:function(){
        return{

        }
    },
    methods:{
        jumpTo(path){
            router.push(path);
        }
    }
}
</script>
