<template>
  <el-steps :active="registerStep" align-center class="register-step">
    <el-step icon="el-icon-user">
      <template #description>
        <i
          v-if="registerStep > 0"
          class="el-icon-check"
          style="font-weight: bold" />
        <i
          v-if="registerStep == 0"
          class="el-icon-location"
          style="font-weight: bold"
      /></template>
    </el-step>
    <el-step icon="el-icon-message">
      <template #description>
        <i
          v-if="registerStep > 1"
          class="el-icon-check"
          style="font-weight: bold" />
        <i
          v-if="registerStep == 1"
          class="el-icon-location"
          style="font-weight: bold" /></template
    ></el-step>
    <el-step icon="el-icon-key">
      <template #description>
        <i
          v-if="registerStep > 2"
          class="el-icon-check"
          style="font-weight: bold" />
        <i
          v-if="registerStep == 2"
          class="el-icon-location"
          style="font-weight: bold" /></template
    ></el-step>
    <el-step icon="el-icon-finished">
      <template #description>
        <i
          v-if="registerStep == 3"
          class="el-icon-location"
          style="font-weight: bold"
      /></template>
    </el-step>
  </el-steps>
</template>

<script>
export default {
  props: {
      registerStep: Number,
  }
};
</script>

<style scoped>
.register-step :deep(.el-step__description) {
  position: absolute;
  top: -8px;
  left: 49%;
  width: 20px;
  height: 16px;
  line-height: 16px;
  padding: 0;
  color: #365638;
}

.register-step :deep(.el-step__line) {
  background: #788f77;
}

.register-step :deep(.el-step__head.is-finish) {
  color: #365638;
  border-color: #365638;
}

.register-step :deep(.el-step__title.is-finish) {
  color: #365638;
  font-weight: 500;
}

.register-step :deep(.el-step__head.is-process) {
  color: #365638;
  border-color: #365638;
}

.register-step :deep(.el-step__title.is-process) {
  color: #365638;
  font-weight: 800;
}

.register-step :deep(.el-step__head.is-wait) {
  color: #788f77;
  border-color: #788f77;
}

.register-step :deep(.el-step__title.is-wait) {
  color: #788f77;
  font-weight: 200;
}
</style>