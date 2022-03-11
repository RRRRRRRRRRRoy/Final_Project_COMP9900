<template>
  <el-radio-group
    v-model="role"
    fill="#365638"
    @change="changeRole"
    ref="registerRole"
    :style="{
      'border-style': 'solid',
      'border-color': roleBoxStyle,
      padding: '1px',
      'border-radius': '5px',
    }"
  >
    <el-col>
      <el-radio-button label="manager"
        ><el-row
          class="role-card"
          justify="center"
          align="middle"
          :style="{ color: managerStyle }"
          ><el-space direction="vertical">
            <el-row style="font-size: 10px">I'M A</el-row>
            <el-row style="font-weight: bold; font-size: 16px">
              MANAGER
            </el-row></el-space
          >
        </el-row>
      </el-radio-button>
    </el-col>
    <el-col>
      <el-radio-button label="tenant"
        ><el-row
          class="role-card"
          justify="center"
          align="middle"
          :style="{ color: tenantStyle }"
          ><el-space direction="vertical">
            <el-row style="font-size: 10px">I'M A</el-row>
            <el-row style="font-weight: bold; font-size: 16px">
              TENANT
            </el-row></el-space
          >
        </el-row>
      </el-radio-button>
    </el-col>
  </el-radio-group>
</template>

<script>
export default {
  props: {
    role: String,
    roleBoxStyle: String,
  },
  // emits: ["update:role"],
  methods: {
    changeRole() {
      this.$emit('changeRole', this.role)
      // this.$refs.registerRole.role = this.role;
      // console.log(this.$refs["registerRole"].role)
    },
  },
  computed: {
    managerStyle() {
      return this.role === "manager" ? "#ffffff" : "#788f77";
    },
    tenantStyle() {
      return this.role === "tenant" ? "#ffffff" : "#788f77";
    },
  },
};
</script>

<style scoped>
.role-card {
  width: 94px;
  height: 40px;
}

:deep(.el-radio-button__inner) {
  border: 1px dotted #788f77;
}

:deep(:first-child .el-radio-button__inner) {
  border-left: 1px dotted #788f77;
}
</style>