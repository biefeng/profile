<template id="sample">
    <div>
        {{menu}}
    </div>
</template>
<script>
    Vue.component("main-content", {
        template: "#sample",
        data() {
            return {
                message: "The is a sample component",
                menu: '{{menu}}'
            }
        }
    });
</script>
<style>

</style>

