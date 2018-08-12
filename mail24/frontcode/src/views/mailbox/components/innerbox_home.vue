<template>
    <div class="mltabview-content">
        <div class="mltabview-panel">
            <div class="m-mllist">
                <div class="list-bg"></div>
                <div class="m-mllist-row">
                    <div class="j-module-top">
                        <div class="j-autoforward message-tip u-alert-warning u-alert-dismissible f-ellipsis f-dn"></div>
                        <div class="j-autoreply message-tip u-alert-warning u-alert-dismissible f-ellipsis f-dn" style="display: none;"></div>
                        <div class="j-defer-tip message-tip u-alert-warning u-alert-dismissible f-ellipsis f-dn"></div>
                        <div class="j-select-all-msg message-tip u-alert-warning f-dn"></div>
                        <div class="toolbar j-toolbar" data-view-cid="view-15" data-view-name="">
                    <span class="u-btn u-btn-default u-btn-round f-fr j-setting"><i class="iconfont iconset"></i></span>
                    <div id="pagination" class="f-fr"><div class="u-page u-page-round"><span class="u-page-btns"><ul class="u-page-menu u-page-menu-hidden" role="pagination-menu"></ul><button class="u-page-btn"><span class="u-page-btntext">1/1</span><span class="u-page-btnsel"></span></button></span><a class="z-current u-page-prev" rel="prev"><span class="iconfont iconprevious"></span></a><a class="z-current u-page-next" rel="next"><span class="iconfont iconnext"></span></a></div></div>

                    <div class="u-btns" data-dropdown="select" role="dropdown">
                        <span class="u-btn u-btn-default j-selectmail">
                            <input type="checkbox" name="checkAll" class="rc-hidden"><i class="checkbox"></i>
                            <span class="iconfont icondown"></span>
                        </span>
                    <ul class="u-menu u-menu-hidden"><li value="select:all"><a href="javascript:void(0);" tabindex="-1">所有</a></li><li class="divider"></li><li value="select:curPage"><a href="javascript:void(0);" tabindex="-1">当前页</a></li><li value="select:unread"><a href="javascript:void(0);" tabindex="-1">未读</a></li><li value="select:read"><a href="javascript:void(0);" tabindex="-1">已读</a></li><li value="select:inverse"><a href="javascript:void(0);" tabindex="-1">反选</a></li><li value="select:none"><a href="javascript:void(0);" tabindex="-1">不选</a></li></ul></div>

                    <div class="u-btns j-viewbtns">
                        <span class="u-btn u-btn-default j-sort" data-dropdown="sort" role="dropdown">排序<span class="iconfont icondown"></span><ul class="u-menu u-menu-hidden"><li value="sort:receivedDate:desc" class="u-menu-choose"><a href="javascript:void(0);" tabindex="-1">按时间从新到旧</a><i class="iconfont iconchoose left u-menu-choose"></i></li><li value="sort:receivedDate:asc"><a href="javascript:void(0);" tabindex="-1">按时间从旧到新</a></li><li class="divider"></li><li value="sort:from:desc"><a href="javascript:void(0);" tabindex="-1">按发件人降序</a></li><li value="sort:from:asc"><a href="javascript:void(0);" tabindex="-1">按发件人升序</a></li><li class="divider"></li><li value="sort:subject:desc"><a href="javascript:void(0);" tabindex="-1">按主题降序</a></li><li value="sort:subject:asc"><a href="javascript:void(0);" tabindex="-1">按主题升序</a></li><li class="divider"></li><li value="sort:flags.attached:asc"><a href="javascript:void(0);" tabindex="-1">按附件降序</a></li><li value="sort:flags.attached:desc"><a href="javascript:void(0);" tabindex="-1">按附件升序</a></li></ul></span>
                        <span class="u-btn u-btn-default" data-dropdown="view" role="dropdown">查看<span class="iconfont icondown"></span><ul class="u-menu u-menu-hidden"><li value="view:all"><a href="javascript:void(0);" tabindex="-1">全部邮件</a></li><li value="view:unread"><a href="javascript:void(0);" tabindex="-1">未读邮件</a></li><li value="view:read"><a href="javascript:void(0);" tabindex="-1">已读邮件</a></li><li class="divider"></li><li value="view:flagged"><i class="iconfont left iconflatcolor flagged label0-0"></i><a href="javascript:void(0);" tabindex="-1">已标记邮件</a></li><li value="view:noflagged"><i class="iconfont left iconflat"></i><a href="javascript:void(0);" tabindex="-1">未标记邮件</a></li><li class="divider"></li><li value="view:urgent"><a href="javascript:void(0);" tabindex="-1">紧急</a></li><li value="view:general"><a href="javascript:void(0);" tabindex="-1">普通</a></li><li value="view:slow"><a href="javascript:void(0);" tabindex="-1">缓慢</a></li><li class="divider"></li><li value="view:attached"><i class="iconfont left iconacc"></i><a href="javascript:void(0);" tabindex="-1">包含附件</a></li><li value="view:noattach"><a href="javascript:void(0);" tabindex="-1">不包含附件</a></li><li class="divider"></li><li value="view:replied"><i class="iconfont left iconback"></i><a href="javascript:void(0);" tabindex="-1">已回复</a></li><li value="view:forwarded"><i class="iconfont left state-icon icon-FORWARDED"></i><a href="javascript:void(0);" tabindex="-1">已转发</a></li></ul></span>
                    </div>

                    <div class="f-ib f-dn j-tgbtns">
                        <span class="u-btn u-btn-default j-deferCompleted" style="display: none;">完成待办</span>
                        <span class="u-btn u-btn-default j-maildelete">删除</span>

                        <div class="u-btns">
                                <span class="u-btn u-btn-default" data-dropdown="move" role="dropdown">移动到<span class="iconfont icondown"></span><ul class="u-menu u-menu-hidden"><li><a href="javascript:void(0);" tabindex="-1">已发送</a></li><li><a href="javascript:void(0);" tabindex="-1">已删除</a></li><li><a href="javascript:void(0);" tabindex="-1">垃圾邮件</a></li><li><a href="javascript:void(0);" tabindex="-1">病毒文件夹</a></li></ul></span>
                            <span class="u-btn u-btn-default" data-dropdown="mark" role="dropdown">标记为<span class="iconfont icondown"></span><ul class="u-menu u-menu-hidden"><li value="mark:read"><a href="javascript:void(0);" tabindex="-1">已读</a></li><li value="mark:unread"><i class="iconfont left iconemail"></i><a href="javascript:void(0);" tabindex="-1">未读</a></li><li class="divider"></li><li value="mark:flagged"><i class="iconfont left iconflatcolor flagged label0-0"></i><a href="javascript:void(0);" tabindex="-1">红旗</a></li><li value="mark:noflagged"><a href="javascript:void(0);" tabindex="-1">取消标记</a></li><li class="divider"></li><li value="mark:priority" class="u-submenu" role="submenu"><a href="javascript:void(0);" tabindex="-1">优先级</a><i class="iconfont iconright right"></i><ul class="u-menu u-menu-hidden"><li value="mark:urgent"><a href="javascript:void(0);" tabindex="-1">紧急</a></li><li value="mark:general"><a href="javascript:void(0);" tabindex="-1">普通</a></li><li value="mark:slow"><a href="javascript:void(0);" tabindex="-1">缓慢</a></li></ul></li><li class="divider"></li><li value="mark:top"><a href="javascript:void(0);" tabindex="-1">置顶邮件</a></li><li value="mark:notop"><a href="javascript:void(0);" tabindex="-1">取消置顶邮件</a></li><li class="divider"></li><li value="defer:set"><i class="iconfont left state-icon icon-mDEFER"></i><a href="javascript:void(0);" tabindex="-1">待办邮件</a></li></ul></span>
                            <span class="u-btn u-btn-default" data-dropdown="more" role="dropdown">更多<span class="iconfont icondown"></span><ul class="u-menu u-menu-hidden"><li value="more:reply"><a href="javascript:void(0);" tabindex="-1">回复</a></li><li value="more:replyall"><a href="javascript:void(0);" tabindex="-1">回复全部</a></li><li class="divider"></li><li value="more:forward"><a href="javascript:void(0);" tabindex="-1">转发</a></li><li value="more:forwarda"><a href="javascript:void(0);" tabindex="-1">附件方式转发</a></li><li class="divider"></li><li value="more:report"><a href="javascript:void(0);" tabindex="-1">举报</a></li><li value="more:reject"><a href="javascript:void(0);" tabindex="-1">拒收邮件</a></li><li value="more:filter"><a href="javascript:void(0);" tabindex="-1">来信分类</a></li><li class="divider"></li><li value="more:sendagain"><a href="javascript:void(0);" tabindex="-1">再次发送</a></li><li value="more:pack"><a href="javascript:void(0);" tabindex="-1">打包下载</a></li><li value="more:realdelete"><a href="javascript:void(0);" tabindex="-1">彻底删除</a></li></ul></span>
                        </div>
                    </div>

                    <span class="u-btn u-btn-default j-mailrefresh">刷新</span>

                </div>
                        <div class="mail-totals j-mail-totals">
                    <div class="totals-info">
                    收件箱(
                    <span class="all-mail">共<span class="number">3</span>封</span>
                    )
                    </div>
                </div>
                        <div class="j-select-count select-count f-dn">
                            <span class="j-desc desc"></span>
                            <a class="j-cancel cancel" href="javascript:void(0);">取消</a>
                        </div>
                    </div>
                </div>

                <div class="m-mllist-row mllist-list-row">
                    <div class="j-module-content j-maillist mllist-list u-scroll">
                        <div class="j-mail-group-wrap">
                            <div class="ist-group-title f-csp">
                                <i class="iconfont iconcollapse f-fr"></i>
                                <span class="j-select-group">更早 (<span class="j-group-length">3</span>)</span>
                            </div>
                            <div class="j-list-group-body">
                                <ul class="list-wrap j-mail-list">
                                    <li class="list-item j-mail read
                                                    display-summary" mid="1:1tbiAQAJEFXEqdgAXgADsl" index="0" fid="1">
                                        <div class="item-content mail-info">
                                            <div class="info-desc">
                                                <div class="info-desc-left">
                                                    <div class="desc-flag">
                                                            <span class="flag-flagged j-flag unflag">
                                                                <i title="设为红旗" class="iconfont iconflat"></i>
                                                            </span>
                                                        <span class="flag-defer unflag">
                                                                <i title="设置待办" class="j-undefer iconfont iconclock"></i>
                                                        </span>
                                                    </div>
                                                    <div class="desc-text">
                                                        <span class="icon"><i class="j-priorityIcon iconfont " title=""></i></span>
                                                        <span class="subject" title="[召回邮件失败] MEMZ彩虹猫病毒/[Recall mail 失败] MEMZ彩虹猫病毒">[召回邮件失败] MEMZ彩虹猫病毒/[Recall mail 失败] MEMZ彩虹猫病毒</span>
                                                    </div>
                                                </div>
                                                <div class="info-desc-right">
                                                    <span class="desc-time">08-09</span>
                                                    
                                                </div>
                                            </div>
                                            <div class="info-summary">
                                                <p class="summary-text">
                                                    <span class="fromto from" data-email="postmaster@xt5-dm100.coremail.cn">
                                                    postmaster
                                                    </span>
                                                    <span class="fromto">：</span>
                                                    <span class="summary">
                                发给751296883@qq.com的邮件召回失败,原因：不支持召回



                                email sent to 751296883@qq.com has been recalled unsucce</span>
                                                </p>
                                                <div class="summary-stat">
                                                    <div class="summary-stat-bg"></div>
                                                    
                                                    
                                                    
                                                </div>
                                            </div>
                                            <div class="info-icon">
                                                <span><i class="j-normalIcon iconfont state-icon icon-SYSTEM" title="系统认证可信任来源"></i></span>
                                            </div>
                                        </div>
                                        <div class="item-chk check-col" title="系统认证可信任来源">
                                            
                                            <input type="checkbox" name="mid" data-draft="" data-fid="1" value="1:1tbiAQAJEFXEqdgAXgADsl" from="postmaster@xt5-dm100.coremail.cn" class="rc-hidden"><i class="checkbox"></i>
                                        </div>
                                        <div class="item-active-border"></div>
                                        <div class="item-divider"></div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    
}
</script>
