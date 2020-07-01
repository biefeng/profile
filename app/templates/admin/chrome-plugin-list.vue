{% raw%}
<template id="chrome-plugin-list">
    <div>
        <el-table
                v-loading="loading"
                ref="multipleTable"
                :data="tableData"
                border
                tooltip-effect="dark"
                style="width: 100%"
                @selection-change="handleSelectionChange"
        >
            <el-table-column
                    type="selection"
                    width="55">
            </el-table-column>
            <el-table-column
                    label="标题">
                <template slot-scope="scope">{{ scope.row.name }}</template>
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="访问量"
                    width="120">
                <template slot-scope="scope">{{ scope.row.num_of_view }}</template>
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="下载量"
                    width="120">
                <template slot-scope="scope">{{ scope.row.source }}</template>
            </el-table-column>
            <el-table-column
                    prop="address"
                    label="分类"
                    width="120"
                    show-overflow-tooltip>
            </el-table-column>
            <el-table-column
                    prop="address"
                    label="下载日期"
                    width="200"
                    show-overflow-tooltip>
                <template slot-scope="scope">{{ scope.row.create_time}}</template>
            </el-table-column>
            <el-table-column
                    prop="address"
                    label="操作"
                    width="180"
                    show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            @click="handleEdit(scope.$index, scope.row)">编辑
                    </el-button>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <pagination :total="total" :size_change="sizeChange" :current_change="list"></pagination>
    </div>
</template>
{% endraw%}
{% include 'base/pagination.vue' %}
<script>
    Vue.component("main-content", {
        template: "#chrome-plugin-list",
        data() {
            return {
                tableData: [],
                option: 1,
                options: [
                    {value: 1, label: "原创"},
                    {value: 2, label: "转载"},
                ],
                query: {},
                pageSize: 10,
                total: 0,
                loading: false
            }
        },
        methods: {
            handleEdit() {
            },
            handleDelete(index, row) {
                this.$http.post("/admin/del-article", {ids: [row.id]}).then(res => {
                    console.log(res)
                })
            },
            handleSelectionChange() {
            },
            list(pageNum, params) {
                this.loading = true
                let assign = Object.assign({pageNumber: pageNum, pageSize: this.pageSize}, params, this.query);
                if (pageNum != undefined) {
                    this.currentPage = pageNum
                }
                this.$http.get("/admin/list-chrome-plugins", {
                    params: assign
                }).then(res => {
                    this.tableData = res.data.list
                    this.total = res.data.total
                    this.loading = false
                }).catch(e => {

                    this.loading = false
                })
            },
            sizeChange(s) {
                this.pageSize = s
                this.list(0, {pageSize: s})
            }
        },
        created() {
            this.list(1)
        }
    });

</script>
<style>
    .query-label {
        padding: 0px 15px 0px 10px;
    }
</style>