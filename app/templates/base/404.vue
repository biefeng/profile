{%raw%}
<template id="err_msg_404">
    <div>
        {{message}}
    </div>
</template>
{%endraw%}
<script>
    Vue.component("main-content", {
        template: "#err_msg_404",
        data() {
            return {
                message: "您要找的页面不存在"
            }
        }
    });
</script>
<style>

</style>

