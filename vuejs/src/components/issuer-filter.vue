<template>
  <v-chip-group
    v-model="custfilterissuers"
    column
    multiple
    active-class="primary--text"
  >
    <v-chip
      filter
      v-for="issuer in issuers"
      :value="issuer.key"
      :key="issuer.key"
      :disabled="disabledIssuer(issuer.key)"
      :class="disabledIssuer(issuer.key) ? 'disabled-issuer' : ''"
      >{{ issuer.name }}</v-chip
    >
  </v-chip-group>
</template>

<script>
module.exports = {
  props: ["value", "warrants"],
  data() {
    return {
      issuers: [
        { key: "SG", name: "Société Générale" },
        { key: "UC", name: "Unicredit" },
      ],
    };
  },
  computed: {
    custfilterissuers: {
      get() {
        var filterissuers = this.value.filter(
          (issuer) => !this.disabledIssuer(issuer)
        );
        //console.log("get " + filterissuers);
        return filterissuers;
      },
      set(val) {
        //console.log("set " + val);
        this.$emit("input", val);
      },
    },
  },
  methods: {
    disabledIssuer(issuer) {
      return (
        this.warrants.filter((warrant) => issuer == warrant["issuer"]).length ==
        0
      );
    },
  },
};
</script>

<style>
.v-chip.v-chip--disabled.disabled-issuer {
  color: white !important;
  background-color: red;
}
</style>