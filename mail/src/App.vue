<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width:100%;
  height:100%;
}
body,html{
  padding:0;
  margin:0;
  width:100%;
  height:100%;
    font-size: 14px;
    line-height: 1.42857143;
    color: #333;
    background-color: #fff;
    overflow: hidden;
}
ul,li,p,h1,h2,h3,h4{
  padding:0;
  margin:0;
}
ul,li{
  list-style:none;
}
.fl_r{
  float:right;
}
.fl_l{
  float:left;
}
</style>
