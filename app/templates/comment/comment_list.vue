{%raw%}
<template id="sample">
    <div>
        {{message}}
    </div>
</template>
{%endraw%}
<script>
    Vue.component("main-content", {
        template: "#sample",
        data() {
            return {
                message: "TODO"
            }
        }
    });
</script>
<style>

</style>

