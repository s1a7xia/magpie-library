# 前端页面模板

本文件按作者 `plus-ui/src/views/demo/demo/index.vue`、`plus-ui/src/views/demo/tree/index.vue` 和对应 `api/demo/*/{index,types}.ts` 蒸馏，供写完整业务页面时按需加载。

模板只提供页面壳、hooks 组合、请求和类型骨架。字段、权限、状态、查询条件和业务流程以当前需求及目标模块的真实实现为准，不把 demo 字段直接带进业务。

## 选择模板

| 场景 | 模板 |
|---|---|
| 普通单表 | 本页“单表列表页” |
| 树形分类 | 本页“树表差异”，再套单表骨架 |
| 只读报表、主从、审批 | 先用 `frontend.md` 的页面形态和现有组件，不硬套 CRUD |

目标模块已有同领域页面时，先读它的查询区、表格、弹窗和 API；保留已有复杂交互，只增量实现当前需求。

## 单表列表页

```vue
<template>
  <div class="p-2 app-container <module>-<business>-page">
    <div class="search-wrap">
      <el-card shadow="hover" class="search-panel" :class="{ 'is-collapsed': !showSearch }">
        <template #header>
          <div class="panel-heading search-panel-toggle" @click.stop="showSearch = !showSearch">
            <div><h3>筛选条件</h3></div>
          </div>
        </template>
        <el-form ref="queryFormRef" :model="queryParams" :inline="true" class="query-form">
          <el-form-item label="名称" prop="name">
            <el-input v-model="queryParams.name" placeholder="请输入名称" clearable @keyup.enter="handleQuery" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
            <el-button icon="Refresh" @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <el-card shadow="hover" class="table-panel">
      <template #header>
        <div class="toolbar-shell">
          <div class="table-heading">
            <h3>Xxx列表</h3>
          </div>
          <div class="toolbar-actions">
            <el-button v-hasPermi="['<module>:<business>:add']" type="primary" plain icon="Plus" @click="handleAdd">
              新增
            </el-button>
            <el-button
              v-hasPermi="['<module>:<business>:edit']"
              type="success"
              plain
              icon="Edit"
              :disabled="single"
              @click="handleUpdate()"
            >
              修改
            </el-button>
            <el-button
              v-hasPermi="['<module>:<business>:remove']"
              type="danger"
              plain
              icon="Delete"
              :disabled="multiple"
              @click="handleDelete()"
            >
              删除
            </el-button>
            <el-button
              v-hasPermi="['<module>:<business>:export']"
              type="warning"
              plain
              icon="Download"
              @click="handleExport"
            >
              导出
            </el-button>
            <right-toolbar v-model:show-search="showSearch" :search="false" @query-table="getList" />
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        border
        class="data-table"
        :data="xxxList"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="名称" align="center" prop="name" />
        <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-tooltip content="修改" placement="top">
              <el-button
                v-hasPermi="['<module>:<business>:edit']"
                link
                type="primary"
                icon="Edit"
                @click="handleUpdate(scope.row)"
              />
            </el-tooltip>
            <el-tooltip content="删除" placement="top">
              <el-button
                v-hasPermi="['<module>:<business>:remove']"
                link
                type="primary"
                icon="Delete"
                @click="handleDelete(scope.row)"
              />
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-show="total > 0"
        v-model:page="queryParams.pageNum"
        v-model:limit="queryParams.pageSize"
        :total="total"
        @pagination="getList"
      />
    </el-card>

    <el-dialog v-model="dialog.visible" :title="dialog.title" width="500px" append-to-body>
      <el-form ref="xxxFormRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button :loading="buttonLoading" type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Xxx" lang="ts">
import { addXxx, delXxx, getXxx, listXxx, updateXxx } from '@/api/<module>/<business>';
import type { XxxForm, XxxQuery, XxxVO } from '@/api/<module>/<business>/types';
import { useLoading } from '@/hooks/async/useLoading';
import { useFormDialog } from '@/hooks/dialog/useFormDialog';
import { useSearchReset } from '@/hooks/form/useSearchReset';
import { useSearchToggle } from '@/hooks/form/useSearchToggle';
import { useTableSelection } from '@/hooks/table/useTableSelection';
import modal from '@/plugins/modal';
import { download as requestDownload } from '@/utils/request';

const xxxList = ref<XxxVO[]>([]);
const buttonLoading = ref(false);
const total = ref(0);
const { loading, withLoading } = useLoading(true);
const { showSearch } = useSearchToggle();
const queryFormRef = ref<ElFormInstance>();
const xxxFormRef = ref<ElFormInstance>();

const initFormData: XxxForm = {
  id: undefined,
  name: undefined
};

const data = reactive<PageData<XxxForm, XxxQuery>>({
  form: { ...initFormData },
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    name: undefined
  },
  rules: {
    name: [{ required: true, message: '名称不能为空', trigger: 'blur' }]
  }
});

const { queryParams, form, rules } = toRefs(data);
const { ids, single, multiple, handleSelectionChange } = useTableSelection<XxxVO>(item => item.id);
const { dialog, resetForm: reset, openDialog, showDialog, closeDialog } = useFormDialog({
  form,
  formRef: xxxFormRef,
  initialFormData: initFormData
});

/** 查询Xxx列表 */
const getList = async () => {
  await withLoading(async () => {
    const res = await listXxx(queryParams.value);
    xxxList.value = res.data?.rows;
    total.value = res.data?.total;
  });
};

/** 取消按钮 */
const cancel = () => {
  reset();
  closeDialog();
};

/** 搜索按钮操作 */
const handleQuery = () => {
  queryParams.value.pageNum = 1;
  getList();
};

const { resetQuery } = useSearchReset({
  queryFormRef,
  queryParams,
  pageNumKey: 'pageNum',
  afterReset: () => {
    handleQuery();
  }
});

/** 新增按钮操作 */
const handleAdd = () => {
  openDialog('添加Xxx');
};

/** 修改按钮操作 */
const handleUpdate = async (row?: Partial<XxxVO>) => {
  reset();
  const xxxId = row?.id || ids.value[0];
  const res = await getXxx(xxxId);
  Object.assign(form.value, res.data);
  showDialog('修改Xxx');
};

/** 提交按钮 */
const submitForm = () => {
  xxxFormRef.value?.validate(async (valid: boolean) => {
    if (valid) {
      buttonLoading.value = true;
      if (form.value.id) {
        await updateXxx(form.value).finally(() => (buttonLoading.value = false));
      } else {
        await addXxx(form.value).finally(() => (buttonLoading.value = false));
      }
      modal.msgSuccess('操作成功');
      closeDialog();
      await getList();
    }
  });
};

/** 删除按钮操作 */
const handleDelete = async (row?: Partial<XxxVO>) => {
  const xxxIds = row?.id || ids.value;
  await modal.confirm('是否确认删除Xxx编号为"' + xxxIds + '"的数据项？');
  await delXxx(xxxIds);
  modal.msgSuccess('删除成功');
  await getList();
};

/** 导出按钮操作 */
const handleExport = () => {
  requestDownload(
    '<module>/<business>/export',
    {
      ...queryParams.value
    },
    `xxx_${new Date().getTime()}.xlsx`
  );
};

onMounted(() => {
  getList();
});
</script>
```

实际页面按字段契约替换搜索项、表格列、弹窗字段和校验；按钮、列和操作按权限与业务状态保留，不为了凑模板增加无用操作。

## 树表差异

树表仍使用上面的查询区、弹窗和 hooks，只替换列表读取、表格属性和父节点交互。

```vue
<el-table
  ref="treeTableRef"
  v-loading="loading"
  class="data-table"
  :data="treeList"
  row-key="id"
  border
  :default-expand-all="isExpandAll"
  :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
>
  <el-table-column label="名称" prop="name" />
</el-table>
```

```ts
import { handleTree } from '@/utils/ruoyi';
import { useTreeTableExpand } from '@/hooks/tree/useTreeTableExpand';

const treeList = ref<XxxVO[]>([]);
const treeTableRef = ref<ElTableInstance>();
const { isExpandAll, handleToggleExpandAll } = useTreeTableExpand<XxxVO>({
  tableRef: treeTableRef,
  data: treeList
});

const getList = async () => {
  await withLoading(async () => {
    const res = await listXxx(queryParams.value);
    treeList.value = handleTree<XxxVO>(res.data, 'id', 'parentId');
  });
};

const handleAdd = (row?: Partial<XxxVO>) => {
  openDialog('添加Xxx');
  form.value.parentId = row?.id || 0;
};
```

- 树表 `Query` 不继承 `PageQuery`，列表接口返回数组，不读 `rows/total`。
- 父节点选择用 `el-tree-select`，先取树选项再回填 `parentId`；新增子节点时从当前行带入父 ID。
- 删除、移动节点前确认子树规则；页面不能自行假设级联删除或移动语义。

## API 文件

```ts
import type { XxxForm, XxxQuery, XxxVO } from '@/api/<module>/<business>/types';
import type { PageResult } from '@/api/types';
import type { AxiosPromise } from '@/utils/api-types';
import request from '@/utils/request';

const base = '/<module>/<business>';

export const listXxx = (query?: XxxQuery): AxiosPromise<PageResult<XxxVO>> => {
  return request({
    url: base + '/list',
    method: 'get',
    params: query
  });
};

export const getXxx = (id: string | number): AxiosPromise<XxxVO> => {
  return request({
    url: base + '/' + id,
    method: 'get'
  });
};

export const addXxx = (data: XxxForm) => {
  return request({
    url: base,
    method: 'post',
    data
  });
};

export const updateXxx = (data: XxxForm) => {
  return request({
    url: base,
    method: 'put',
    data
  });
};

export const delXxx = (id: string | number | Array<string | number>) => {
  return request({
    url: base + '/' + id,
    method: 'delete'
  });
};
```

## 类型文件

```ts
export interface XxxVO {
  /** 主键 */
  id: string | number;

  /** 名称 */
  name: string;
}

export interface XxxForm extends BaseEntity {
  /** 主键 */
  id?: string | number;

  /** 名称 */
  name?: string;
}

export interface XxxQuery extends PageQuery {
  /** 名称 */
  name?: string;
}
```

- `VO` 字段必填；`Form` 继承 `BaseEntity` 且字段全部可选；`Query` 继承 `PageQuery` 且条件可选。
- 主键和关联 ID 用 `string | number`，不要只写 `number`，避免雪花 ID 丢精度。
- 字段名与后端 BO/VO 完全一致；日期范围保留 `Query.params`，不要改成平铺的 `beginTime` / `endTime`。
- 纯类型导入优先 `import type`；若目标模块已统一使用普通导入，保持该模块风格，不混改。

## 交付前检查

- [ ] 页面使用 `p-2 app-container`、搜索区、表格区和分页的现有页面壳。
- [ ] 查询、表格、弹窗和表单字段来自同一份业务契约。
- [ ] 使用了现有 `useLoading`、`useFormDialog`、`useSearchReset`、`useSearchToggle`、`useTableSelection`。
- [ ] 编辑先拉详情再回填，新增先重置；提交失败保留输入并恢复按钮 loading。
- [ ] 删除有确认和刷新；树表新增子节点携带 `parentId`。
- [ ] 权限字符在菜单 SQL、后端注解和 `v-hasPermi` 三处一致。
- [ ] 页面可见改动只标记 `Dev Complete`，由用户发起 `page-acceptance`，不把构建通过说成验收通过。
