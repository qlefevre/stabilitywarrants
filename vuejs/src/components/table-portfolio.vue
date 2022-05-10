<template>
  <v-data-table
    :headers="this.headers"
    :items="this.items"
    :sort-by="['maturitejours', 'sous-jacent', 'plage']"
    :sort-desc="[false, false, true, false]"
    :footer-props="{ 'items-per-page-options': [-1, 50, 100] }"
    multi-sort
    dense
    group-by="maturitejours"
    class="elevation-1"
    mobile-breakpoint="100"
  >
    <template v-slot:item.isin="{ item }">
      <isin v-model="item"></isin>
    </template>
    <template v-slot:item.bornes="{ item }">
      {{ item.bornebasse }} {{ item.bornehaute }}
    </template>
    <template v-slot:item.perfmin="{ item }">
      <span :style="getPerfStyle(item.perfmin)">{{ item.perfmin }}</span>
    </template>
    <template v-slot:item.perfmax="{ item }">
      <span :style="getPerfStyle(item.perfmax)">{{ item.perfmax }}</span>
    </template>
    <template v-slot:item.pvlatentes="{ item }">
      <span :style="getPvStyle(item.pvlatentes)">{{ item.pvlatentes }}</span>
    </template>
    <template v-slot:item.pvpotentielles="{ item }">
      <span :style="getPvStyle(item.pvpotentielles)">{{
        item.pvpotentielles
      }}</span>
    </template>
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
          :style="
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
          :style="getPvStyle(pvPotentiellesPourcentage(items[0].maturitejours))"
        >
          {{ pvPotentiellesPourcentage(items[0].maturitejours) }}</span
        >
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <span
          :style="
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
  </v-data-table>
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
    getPerfStyle(perf) {
      if (perf < 7) return "color:red;font-weight:bold;";
      else if (perf < 12) return "color:orange;font-weight:bold;";
      else return "";
    },
    getPvStyle(pv) {
      if (pv < 0) return "color:red;";
      return "color:forestgreen;";
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
    isin: httpVueLoader("vuejs/src/components/isin.vue"),
  },
};
</script>

<style>
</style>