<template>
  <div class="welcome_box">
      <div class="mlsidebar">
          <Menubar></Menubar>
      </div>
      <div class="mlmain">
            <router-view></router-view>    
      </div>
  </div>
</template>
<script>
export default {
    
}
</script>
<style>
.welcome_box{
    width:100%;
    height:100%;
    position:relative;
}
.mlsidebar {
    position: relative;
    width: 199px;
    height: 100%;
    border-right: 1px solid #d4d7d9;
    text-align: center;
}
.mlmain {
    position: absolute;
    left: 200px;
    right: 0;
    top: 0;
    bottom: 0;
}
</style>

