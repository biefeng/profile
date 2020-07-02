{% raw %}
<template id="article_list">
    <div class="main-wrap-outer">
        <div class="main-wrap-inner">
            
        </div>
    </div>
</template>

{% endraw %}
<script>
    Vue.component("main-content", {
        template: "#article_list",
        data() {
            return {
                message: "The is a sample component"
            }
        }
    });
</script>
<style>

</style>

