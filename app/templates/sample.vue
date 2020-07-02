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
                message: "The is a sample component"
            }
        }
    });
</script>
<style>

</style>

