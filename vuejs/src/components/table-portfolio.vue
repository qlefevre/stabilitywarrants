<template>
  <table-stabilitywarrants
    :headers="this.headers"
    :items="this.items"
    v-bind="$attrs"
    group-by="maturitejours"
  >
    <template v-slot:group.header="{ items, isOpen, toggle }">
      <th class="group-maturite-jours" colspan="4">
        <span class="hidden-lg-and-up"
          >{{ headers[5].text }}: {{ items[0].maturitejours }} jours
          <br /></span
        >Montant: {{ sumWarrants(items[0].maturitejours) }}
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <v-tooltip right>
          <template v-slot:activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on">
              {{ items[0].maturitejours }} jours</span
            >
          </template>
          <span
            >{{ maturiteJoursOuvrables(items[0].maturitejours) }} jours
            ouvrables</span
          >
        </v-tooltip>
      </th>
      <th colspan="1"></th>
      <!-- bornes -->
      <th class="hidden-md-and-down" colspan="2"></th>
      <th class="group-maturite-jours">
        {{ sumCol(items[0].maturitejours, (warrant) => warrant.quantite, 0) }}
      </th>
      <th class="group-maturite-jours">
        {{ prixDeRevientMoyen(items[0].maturitejours) }}
      </th>
      <th></th>
      <th class="group-maturite-jours">
        <span
          :class="
            getPvStyle(
              sumCol(items[0].maturitejours, (warrant) => warrant.pvlatentes, 2)
            )
          "
        >
          {{
            sumCol(items[0].maturitejours, (warrant) => warrant.pvlatentes, 2)
          }}</span
        >
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <span
          :class="getPvStyle(pvPotentiellesPourcentage(items[0].maturitejours))"
        >
          {{ pvPotentiellesPourcentage(items[0].maturitejours) }}</span
        >
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <span
          :class="
            getPvStyle(
              sumCol(
                items[0].maturitejours,
                (warrant) => warrant.pvpotentielles,
                2
              )
            )
          "
        >
          {{
            sumCol(
              items[0].maturitejours,
              (warrant) => warrant.pvpotentielles,
              2
            )
          }}</span
        >
      </th>
    </template>
  </table-stabilitywarrants>
</template>

<script>
module.exports = {
  props: ["items", "headers"],
  computed: {
    portfolioWarrantsTotalAmount() {
      return this.items
        .map((warrant) => warrant.quantite * warrant.prixrevient)
        .reduce((s0, s1) => Number(s0) + Number(s1), 0)
        .toFixed(2);
    },
  },
  methods: {
    getStyle(perf) {
      if (perf < 7) return "red-value";
      else if (perf < 12) return "orange-value";
      else return "";
    },
    getPvStyle(pv) {
      if (pv < 0) return "red-pv";
      return "green-pv";
    },

    sumCol(maturitejours, applyfunction, fixed) {
      return this.items
        .filter((warrant) => warrant.maturitejours == maturitejours)
        .map(applyfunction)
        .reduce((s0, s1) => Number(s0) + Number(s1), 0)
        .toFixed(fixed);
    },
    sumWarrants(maturitejours) {
      var sumWarrants = this.sumCol(
        maturitejours,
        (warrant) => warrant.quantite * warrant.prixrevient,
        2
      );
      var totalAmount = this.portfolioWarrantsTotalAmount;
      // return sumWarrants.toString().padStart(8, ' ').replaceAll(' ', '&nbsp;') +
      return (
        sumWarrants +
        " (" +
        ((sumWarrants / totalAmount) * 100).toFixed(2) +
        "%)"
      );
    },
    pvPotentiellesPourcentage(maturitejours) {
      var sumWarrants = this.sumCol(
        maturitejours,
        (warrant) => warrant.quantite * warrant.prixrevient,
        2
      );
      var quantite = this.sumCol(
        maturitejours,
        (warrant) => warrant.quantite,
        0
      );
      return (((quantite * 10) / sumWarrants - 1) * 100).toFixed(2);
    },
    prixDeRevientMoyen(maturitejours) {
      var sumWarrants = this.sumCol(
        maturitejours,
        (warrant) => warrant.quantite * warrant.prixrevient,
        2
      );
      var quantite = this.sumCol(
        maturitejours,
        (warrant) => warrant.quantite,
        0
      );
      return (sumWarrants / quantite).toFixed(2);
    },
    maturiteJoursOuvrables(maturitejours) {
      var weeks = Math.round(maturitejours / 7);
      var days = maturitejours - 2 * weeks;
      return days;
    },
  },
  components: {
    "table-stabilitywarrants": httpVueLoader(
      "vuejs/src/components/table-stabilitywarrants.vue"
    ),
  },
};
</script>

<style>
@import "table.css";
</style>