{% raw%}
<template id="pagination-template">
    <div class="pagination-container">
        <el-pagination
                background
                layout="total, prev, pager, next"
                :total="total"
                :page-size="pageSize"
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
        props: ['total', 'size_change', 'current_change', 'pageSize'],
    });

</script>
<style>
    .pagination-container {
        display: flex;
        padding: 20px;
        justify-content: flex-end;
    }
</style>