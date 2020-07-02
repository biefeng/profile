{% raw%}
<template id="article-list">
    <div>
        <el-row :gutter="20">
            <el-col :xs="{span:15,offset:0}" :sm="{span:9,offset:0}" :md="{span:6}" :lg="{span:5}">
                <span class="query-label">来源:</span>
                <el-select v-model="query.source" placeholder="请选择">
                    <el-option
                            v-for="item in sources"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :xs="{span:15,offset:0}" :sm="{span:9,offset:0}" :md="{span:6}" :lg="{span:5}">
                <span class="query-label">分类:</span>
                <el-select v-model="query.category" placeholder="请选择">
                    <el-option
                            v-for="item in categories"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :xs="{span:15,offset:0}" :sm="{span:9,offset:0}" :md="{span:5}">
                <el-button type="primary" @click="list(1,query)">查询</el-button>
                <el-button type="danger">批量删除</el-button>
            </el-col>
        </el-row>

        <el-table
                v-loading="loading"
                border
                :stripe="true"
                ref="multipleTable"
                :data="tableData"
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
                <template slot-scope="scope">{{ scope.row.title }}</template>
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="访问量"
                    width="120">
                <template slot-scope="scope">{{ scope.row.num_of_view }}</template>
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="来源"
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
                    label="发表日期"
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
        template: "#article-list",
        data() {
            return {
                tableData: [],
                option: 1,
                sources: [
                    {value: 1, label: "原创"},
                    {value: 2, label: "转载"},
                    {value: 3, label: "翻译"},
                ],
                categories: [
                    {value: 1, label: "未分类"},
                ],
                query: {},
                pageSize: 10,
                currentPage: 1,
                total: 0,
                loading: false
            }
        },
        methods: {
            handleEdit() {
            },
            handleDelete(index, row) {
                this.$http.post("/admin/del-article", {ids: [row.id]}).then(res => {
                    this.list(1)
                }).catch(e => {
                    console.log(e)
                })
            },
            handleSelectionChange() {
            },
            list(pageNum, params) {
                this.loading = true
                let assign = Object.assign({pageNumber: pageNum, pageSize: this.pageSize}, params);
                if (pageNum != undefined) {
                    this.currentPage = pageNum
                }
                this.$http.get("/article/list-data", {
                    params: assign
                }).then(res => {
                    this.tableData = res.data.list
                    this.total = res.data.total
                    this.loading = false
                }).catch(e => {
                    this.$message.error(e)
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


    .el-col {
        border-radius: 4px;
        margin-bottom: 20px;
    }
</style>