{%raw%}
<template id="component_not_found">
    <div>
        {{message}}
    </div>
</template>
{%endraw%}
<script>
    Vue.component("main-content", {
        template: "#component_not_found",
        data() {
            return {
                message: "The component not  found"
            }
        }
    });
</script>
<style>

</style>

