<template>
  <v-chip-group
    label="Maturité"
    v-model="filtermaturity"
    column
    multiple
    active-class="primary--text"
  >
    <v-chip
      filter
      v-for="month in monthsFromMaturities"
      :value="month"
      :key="month"
    >
      {{ months[month] }}
    </v-chip>
  </v-chip-group>
</template>

<script>
module.exports = {
  props: ["value", "warrants"],
  data() {
    return {
      months: [
        "None",
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
      ],
    };
  },
  computed: {
    filtermaturity: {
      get() {
        /*var mFM = this.monthsFromMaturities();
        var filtermaturity0 = mFM.includes(this.value) ? this.value : mFM[0];*/
        var filtermaturity0 = this.value;
        //console.log("maturity->get: " + filtermaturity0 + " (" + this.value + ")");
        return filtermaturity0;
      },
      set(val) {
        //console.log("maturity->set: " + val);
        this.$emit("input", val);
      },
    },
    monthsFromMaturities() {
      //console.log(this.warrants.map((sw) => sw["maturite"]));
      var maturities = this.warrants
        .map((sw) => sw["maturite"])
        .map((str) => str.substring(str.indexOf("/") + 1, str.lastIndexOf("/")))
        .map((str) => Number(str));
      maturities = Array.from(new Set(maturities));
      maturities.sort((a, b) => a - b);
      // console.log("maturites " + maturities);
      return maturities;
    },
  },
};
</script>

<style>
</style>
