{% raw%}
<template id="pagination-template">
    <div class="pagination-container">

        <el-pagination
                background
                layout="total, prev, pager, next"
                :total="total"
                :page-size="page_size"
                :size-change="size_change"
                @current-change="current_change"
        >
        </el-pagination>
    </div>
</template>

{% endraw%}
<script>
    Vue.component("pagination", {
        template: "#pagination-template",
        props: ['total', 'size_change', 'current_change', 'page_size'],
    });

</script>
<style>
    .pagination-container {
        display: flex;
        padding: 20px;
        justify-content: flex-end;
    }
</style>