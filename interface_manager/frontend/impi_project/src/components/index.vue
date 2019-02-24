<template>
  <div>
    hello I am index
  </div>
</template>

<script>
  import {get_user} from "../requests/user";

  export default {
    name: 'index',
    data() {
      return {
        current_user: {},
      }
    },
    mounted() {
      get_user().then(data => {
        if(true === data.success){
          this.current_user = data.data;
        }else{
          this.$router.push('/login');
          // this.$message.error(data.message);
        }
      })
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
