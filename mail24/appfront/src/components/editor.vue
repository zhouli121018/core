<template>
  <editor  :height="frame_height" width="100%" :content="content"



                    >

                </editor>
</template>
<script>
  export default {
    name: 'Editor',
    data () {
      return {

      }
    },
    props: {
      content: '',
      frame_height: ''
    },
    methods: {
      onContentChange (val) {
        this.content = val
      },
      afterChange (val) {
        console.log(val)
      }
    }
  }
</script>
