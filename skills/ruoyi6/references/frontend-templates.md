# React 页面模板

本文件按 `plus-ui-React/src/pages/demo/demo/index.tsx`、`src/pages/demo/tree/index.tsx`、对应 API/types 和 `gen/*.ftl` 蒸馏，供标准单表和树表页面按需加载。前端 API、types 和页面骨架只在本文件维护一份；`frontend.md` 只负责规则和复用边界。

模板只提供页面壳、hooks 组合、请求和类型骨架。字段、权限、状态、查询条件和业务流程以当前需求和已确认契约为准；目标模块只用于核对字段、路由、权限和集成事实，不把 demo 字段或业务页面写法直接带进新需求。

## 选择模板

| 场景 | 模板 |
|---|---|
| 普通单表 | 本页“单表页面” |
| 树形分类 | 本页“树表差异”，再套单表骨架 |
| 只读报表、主从、审批 | 先用 `frontend.md` 的页面形态和现有组件，不硬套 CRUD |

维护目标模块已有页面时，先读它的查询区、表格、弹窗和 API，保留已有复杂交互，只增量实现当前需求。新建页面仍按作者 demo 和公共组件搭建。

## 单表页面

```tsx
import { DeleteOutlined, DownloadOutlined, EditOutlined, PlusOutlined } from '@ant-design/icons';
import {
  ModalForm,
  PageContainer,
  ProFormText,
  ProTable,
  type ActionType,
  type ProColumns
} from '@ant-design/pro-components';
import { useBoolean } from 'ahooks';
import { Button, Form, message, Popconfirm } from 'antd';
import { useRef, useState } from 'react';
import type { XxxForm, XxxQuery, XxxVO } from '@/api/<module>/<business>/types';
import { addXxx, delXxx, getXxx, listXxx, updateXxx } from '@/api/<module>/<business>';
import RowActions from '@/components/common/RowActions';
import { useTableExport } from '@/hooks/useTableExport';
import { useTableScroll } from '@/hooks/useTableScroll';
import { useTableSelection } from '@/hooks/useTableSelection';
import { useUserStore } from '@/stores/userStore';
import { hasPermi } from '@/utils/permission';
import { toPageQuery, toTableData } from '@/utils/ruoyi';

const defaultXxxForm: XxxForm = {};

export default function XxxPage() {
  const actionRef = useRef<ActionType | undefined>(undefined);
  const { tableScroll } = useTableScroll(760);
  const [form] = Form.useForm<XxxForm>();
  const userInfo = useUserStore(state => state.userInfo);
  const { ids, selectedOne, handleSelectionChange, clearSelection } = useTableSelection<XxxVO>(row => row.id);
  const [modalOpen, { setTrue: openModal, setFalse: closeModal }] = useBoolean(false);
  const [modalTitle, setModalTitle] = useState('');
  const { updateExportParams, exportFile } = useTableExport();

  const canAdd = hasPermi(userInfo, ['<module>:<business>:add']);
  const canEdit = hasPermi(userInfo, ['<module>:<business>:edit']);
  const canRemove = hasPermi(userInfo, ['<module>:<business>:remove']);
  const canExport = hasPermi(userInfo, ['<module>:<business>:export']);

  const openAdd = () => {
    form.resetFields();
    form.setFieldsValue(defaultXxxForm);
    setModalTitle('添加Xxx');
    openModal();
  };

  const openEdit = async (row?: XxxVO) => {
    const target = row || selectedOne;
    if (!target?.id) return;
    const res = await getXxx(target.id);
    form.resetFields();
    form.setFieldsValue(res.data);
    setModalTitle('修改Xxx');
    openModal();
  };

  const submitForm = async (values: XxxForm) => {
    values.id ? await updateXxx(values) : await addXxx(values);
    message.success('操作成功');
    form.resetFields();
    actionRef.current?.reload();
    return true;
  };

  const remove = async (row?: XxxVO) => {
    await delXxx(row?.id || ids);
    message.success('删除成功');
    clearSelection();
    actionRef.current?.reloadAndRest?.();
  };

  const columns: ProColumns<XxxVO>[] = [
    { title: '名称', dataIndex: 'name' },
    {
      title: '操作',
      valueType: 'option',
      width: 92,
      fixed: 'right',
      render: (_, row) => (
        <RowActions
          actions={[
            canEdit && { key: 'edit', label: '修改', icon: <EditOutlined />, onClick: () => openEdit(row) },
            canRemove && {
              key: 'delete',
              label: '删除',
              icon: <DeleteOutlined />,
              danger: true,
              confirm: `是否确认删除Xxx编号为"${row.id}"的数据项？`,
              onClick: () => remove(row)
            }
          ]}
        />
      )
    }
  ];

  return (
    <PageContainer title="Xxx">
      <ProTable<XxxVO, XxxQuery>
        actionRef={actionRef}
        rowKey="id"
        columns={columns}
        scroll={tableScroll}
        search={{ labelWidth: 90 }}
        pagination={{ defaultPageSize: 10, showSizeChanger: true }}
        rowSelection={{ selectedRowKeys: ids, onChange: handleSelectionChange }}
        request={async params => {
          const query = toPageQuery(params);
          updateExportParams(query);
          const res = await listXxx(query);
          return toTableData(res);
        }}
        toolbar={{ title: 'Xxx列表' }}
        toolBarRender={() => [
          canAdd && (
            <Button key="add" type="primary" icon={<PlusOutlined />} onClick={openAdd}>
              新增
            </Button>
          ),
          canEdit && (
            <Button key="edit" disabled={!selectedOne} icon={<EditOutlined />} onClick={() => openEdit()}>
              修改
            </Button>
          ),
          canRemove && (
            <Popconfirm
              key="delete"
              title={`是否确认删除Xxx编号为"${ids}"的数据项？`}
              onConfirm={() => remove()}
            >
              <Button danger disabled={!ids.length} icon={<DeleteOutlined />}>
                删除
              </Button>
            </Popconfirm>
          ),
          canExport && (
            <Button
              key="export"
              icon={<DownloadOutlined />}
              onClick={() => exportFile('/<module>/<business>/export', () => `xxx_${Date.now()}.xlsx`)}
            >
              导出
            </Button>
          )
        ]}
      />

      <ModalForm<XxxForm>
        title={modalTitle}
        open={modalOpen}
        width={560}
        form={form}
        layout="vertical"
        initialValues={defaultXxxForm}
        modalProps={{ destroyOnHidden: true, onCancel: closeModal }}
        onOpenChange={open => !open && closeModal()}
        onFinish={submitForm}
      >
        <ProFormText name="id" hidden />
        <ProFormText name="name" label="名称" rules={[{ required: true, message: '名称不能为空' }]} />
      </ModalForm>
    </PageContainer>
  );
}
```

实际页面按字段契约替换搜索项、表格列、弹窗字段和校验。按钮、列和操作按权限与业务状态保留，不为了凑模板增加无用操作。

## 日期范围

```tsx
import { useDateRangeQuery } from '@/hooks/useDateRangeQuery';

const { applyDateRange: applyCreateTimeDateRange } = useDateRangeQuery();

// columns 里增加只用于搜索的列
{
  title: '创建时间',
  dataIndex: 'createTimeRange',
  valueType: 'dateTimeRange',
  hideInTable: true
}

request={async params => {
  const { createTimeRange, ...tableParams } = params;
  const query = applyCreateTimeDateRange(toPageQuery(tableParams), createTimeRange);
  updateExportParams(query);
  const res = await listXxx(query);
  return toTableData(res);
}}
```

日期范围必须写入 `query.params.begin*/end*`，不要平铺成普通字段。

## 字典与状态

```tsx
import { Switch } from 'antd';
import DictTag from '@/components/common/DictTag';
import { useDict } from '@/hooks/useDict';
import { dictOptions } from '@/utils/dict';

const dicts = useDict('sys_normal_disable');

// 查询/表单
fieldProps: { options: dictOptions(dicts.sys_normal_disable) }

// 列表展示
render: (_, row) => <DictTag options={dicts.sys_normal_disable} value={row.status} />

// 可编辑状态
<Switch checked={row.status === '0'} onChange={checked => handleStatusChange(row, checked)} />
```

状态变更先确认、再调用接口；失败时恢复原值并刷新。不要把字典中文硬编码在页面。

## 树表差异

树表 API 返回 `R<XxxVO[]>`，`Query` 不继承 `PageQuery`，页面用 `handleTree` 建树，`ProTable` 关闭分页并配置 `expandable`。

```tsx
import { SortAscendingOutlined } from '@ant-design/icons';
import { ProFormTreeSelect } from '@ant-design/pro-components';
import { useMemo, useState } from 'react';
import { useTreeTableExpand } from '@/hooks/useTreeTableExpand';
import { handleTree } from '@/utils/ruoyi';

interface TreeSelectNode {
  title: string;
  value: string | number;
  children?: TreeSelectNode[];
}

function toTreeSelectData(
  getTitle: (node: XxxVO) => string,
  nodes: XxxVO[],
  excludedIds: Set<string | number> = new Set()
): TreeSelectNode[] {
  return nodes
    .filter(node => !excludedIds.has(node.id))
    .map(node => ({
      title: getTitle(node),
      value: node.id,
      children: node.children?.length ? toTreeSelectData(getTitle, node.children, excludedIds) : undefined
    }));
}

function collectSubtreeIds(nodes: XxxVO[], rootId: string | number): Set<string | number> {
  const result = new Set<string | number>();
  const walk = (items: XxxVO[]) => {
    for (const item of items) {
      if (item.id === rootId) {
        const collect = (node: XxxVO) => {
          result.add(node.id);
          node.children?.forEach(collect);
        };
        collect(item);
        return true;
      }
      if (item.children?.length && walk(item.children)) return true;
    }
    return false;
  };
  walk(nodes);
  return result;
}

const [treeOptions, setTreeOptions] = useState<XxxVO[]>([]);
const [tableRows, setTableRows] = useState<XxxVO[]>([]);
const [excludedTreeIds, setExcludedTreeIds] = useState<Set<string | number>>(new Set());
const { expandAll, expandedRowKeys, onExpandedRowsChange, syncExpandedRows, toggleExpandAll } =
  useTreeTableExpand<XxxVO>(row => row.id);
const treeSelectData = useMemo(
  () => [
    {
      title: '顶级节点',
      value: 0,
      children: toTreeSelectData(node => node.name, treeOptions, excludedTreeIds)
    }
  ],
  [treeOptions, excludedTreeIds]
);

const loadTreeOptions = async () => {
  const res = await listXxx();
  setTreeOptions(handleTree<XxxVO>(res.data || [], 'id', 'parentId'));
};

const openAdd = async (row?: XxxVO) => {
  await loadTreeOptions();
  setExcludedTreeIds(new Set());
  form.resetFields();
  form.setFieldsValue({ ...defaultXxxForm, parentId: row?.id || 0 });
  setModalTitle('添加Xxx');
  openModal();
};

const openEdit = async (row: XxxVO) => {
  const [listRes, detailRes] = await Promise.all([listXxx(), getXxx(row.id)]);
  const rows = handleTree<XxxVO>(listRes.data || [], 'id', 'parentId');
  setTreeOptions(rows);
  setExcludedTreeIds(collectSubtreeIds(rows, row.id));
  form.resetFields();
  form.setFieldsValue(detailRes.data);
  setModalTitle('修改Xxx');
  openModal();
};

<ProTable<XxxVO, XxxQuery>
  actionRef={actionRef}
  rowKey="id"
  columns={columns}
  scroll={tableScroll}
  pagination={false}
  search={{ labelWidth: 90 }}
  expandable={{
    expandedRowKeys,
    onExpandedRowsChange
  }}
  request={async params => {
    const res = await listXxx({ name: params.name });
    const rows = handleTree<XxxVO>(res.data || [], 'id', 'parentId');
    setTableRows(rows);
    syncExpandedRows(rows, expandAll);
    return { data: rows, total: rows.length, success: true };
  }}
  toolbar={{ title: 'Xxx列表' }}
  toolBarRender={() => [
    canAdd && (
      <Button key="add" type="primary" icon={<PlusOutlined />} onClick={() => openAdd()}>
        新增
      </Button>
    ),
    <Button key="expand" icon={<SortAscendingOutlined />} onClick={() => toggleExpandAll(tableRows)}>
      展开/折叠
    </Button>
  ]}
/>;

<ProFormTreeSelect
  name="parentId"
  label="上级节点"
  fieldProps={{
    allowClear: true,
    treeDefaultExpandAll: true,
    treeData: treeSelectData
  }}
/>;
```

父节点树选项从平铺数据建树，编辑时排除自身及子树。删除、移动节点前确认后端子树规则，页面不能自行假设级联删除或移动语义。

树表导出方法与单表不同：作者示例 `TestTreeController.export` 使用 `GET /export`，而 `download()` 固定 POST。树表页面加导出时，先用 `request({ method: 'get', responseType: 'blob' })` 取 Blob，再用 `saveValidatedBlob` 保存；或先把 `download` 扩展成可传 method，不能直接复用固定 POST 的 `exportFile`。

## API 文件

```ts
import type { PageResult, R } from '@/api/types';
import request from '@/api/request';
import type { XxxForm, XxxQuery, XxxVO } from './types';

export function listXxx(query?: XxxQuery) {
  return request<R<PageResult<XxxVO>>>({
    url: '/<module>/<business>/list',
    method: 'get',
    params: query
  });
}

export function getXxx(id: string | number) {
  return request<R<XxxVO>>({
    url: '/<module>/<business>/' + id,
    method: 'get'
  });
}

export function addXxx(data: XxxForm) {
  return request<R>({
    url: '/<module>/<business>',
    method: 'post',
    data
  });
}

export function updateXxx(data: XxxForm) {
  return request<R>({
    url: '/<module>/<business>',
    method: 'put',
    data
  });
}

export function delXxx(id: string | number | Array<string | number>) {
  return request<R>({
    url: '/<module>/<business>/' + id,
    method: 'delete'
  });
}
```

树表列表的返回类型改为 `request<R<XxxVO[]>>`，且不带分页参数。

## 类型文件

```ts
import type { BaseEntity, PageQuery } from '@/api/types';

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

- `VO`、`Form`、`Query` 的可空性按后端 VO/BO 契约映射，示例里的可选标记不是通用规则。`Form` 通常继承 `BaseEntity`，`Query` 通常继承 `PageQuery`。前端 `BaseEntity` 不含 `createDept`，需要时在 `Form` 中显式声明。
- 树表 `Query` 不继承 `PageQuery`，`VO` 增加 `parentId` 和可选 `children`，`Form` 增加 `parentId`，同时补齐后端契约。单表模板不预带树字段。
- 主键和关联 ID 用 `string | number`，避免雪花 ID 丢精度。
- 字段名与后端 BO/VO 完全一致；日期范围保留 `Query.params`。
- 纯类型导入用 `import type`；若目标模块已统一使用普通导入，保持该模块风格。

## 交付前检查

- [ ] 页面使用 `PageContainer`、`ProTable` 和 `ModalForm` 的现有页面壳。
- [ ] 查询、表格、弹窗和表单字段来自同一份业务契约。
- [ ] 所需行为已复用对应 hooks；不为凑清单引入日期范围、字典或树等未使用能力。
- [ ] 编辑先拉详情再回填，新增先重置；提交失败保留输入并恢复提交状态。
- [ ] 删除有确认和刷新；树表新增子节点携带 `parentId`。
- [ ] 权限字符在菜单 SQL、后端注解和 `hasPermi` 三处一致。
- [ ] 页面已登记到 `dynamicPage.tsx`。
- [ ] 页面可见改动只标记 `Dev Complete`，由用户发起 `page-acceptance`，不把构建通过说成验收通过。
