{%raw%}
<template id="error_500">
    <div>
        {{message}}
    </div>
</template>
{%endraw%}
<script>
    Vue.component("main-content", {
        template: "#error_500",
        data() {
            return {
                message: "抱歉，服务器内部出现错误。"
            }
        }
    });
</script>
<style>

</style>

