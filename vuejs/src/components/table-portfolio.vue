<template>
  <table-stabilitywarrants :headers="this.headers" :items="this.items" v-bind="$attrs" group-by="maturitejours">
  
    <!-- headers -->
    <template v-slot:group.header="{ items, isOpen, toggle }">
      <th class="group-maturite-jours" colspan="4">
        <span class="hidden-lg-and-up">{{ headers[5].text }}: {{ items[0].maturitejours }} jours<br /></span>
        Montant: {{ sumWarrants(items[0].maturitejours) }}
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <v-tooltip right>
          <template v-slot:activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on"> {{ items[0].maturitejours }} jours</span>
          </template>
          <span>{{ maturiteJoursOuvrables(items[0].maturitejours) }} jours ouvrables</span>
        </v-tooltip>
      </th>
      <th colspan="1"></th>
      <!-- bornes -->
      <th class="hidden-md-and-down" colspan="2"></th>
      <th class="group-maturite-jours">{{ sumCol(items[0].maturitejours, (warrant) => warrant.quantite, 0) }}</th>
      <th class="group-maturite-jours">{{ prixDeRevientMoyen(items[0].maturitejours) }}</th>
      <th></th>
      <th class="group-maturite-jours">
        <span :class="getPvStyle(sumCol(items[0].maturitejours, (warrant) => warrant.pvlatentes, 2))">
          {{ sumCol(items[0].maturitejours, (warrant) => warrant.pvlatentes, 2) }}
        </span>
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <span :class="getPvStyle(pvLatentesPourcentage(items[0].maturitejours))">
          {{ pvLatentesPourcentage(items[0].maturitejours) }}
        </span>
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <span :class="getPvStyle(sumCol(items[0].maturitejours, (warrant) => warrant.pvpotentielles, 2))">
          {{ sumCol(items[0].maturitejours, (warrant) => warrant.pvpotentielles, 2) }}
        </span>
      </th>
      <th class="group-maturite-jours hidden-md-and-down">
        <span :class="getPvStyle(pvPotentiellesPourcentage(items[0].maturitejours))">
          {{ pvPotentiellesPourcentage(items[0].maturitejours) }}
        </span>
      </th>
      <th class="hidden-md-and-down" colspan="2"></th>
    </template>
    
    <!-- portfolio -->
    <template v-slot:item.pvlatentes="{ item }">
      <span :class="getPvStyle(item.pvlatentes)">{{ item.pvlatentes }}</span>
    </template>
    <template v-slot:item.pvlatentespercentage="{ item }">
      <span :class="getPvStyle(item.pvlatentespercentage)">{{ item.pvlatentespercentage }}</span>
    </template>
    <template v-slot:item.pvpotentielles="{ item }">
      <span :class="getPvStyle(item.pvpotentielles)">{{ item.pvpotentielles }}</span>
    </template>
    <template v-slot:item.pvpotentiellespercentage="{ item }">
      <span :class="getPvStyle(item.pvpotentiellespercentage)">{{ item.pvpotentiellespercentage }}</span>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon>mdi-clock-end</v-icon>
    </template>
    
  </table-stabilitywarrants>
</template>

<script>
module.exports = {
  props: ["items", "headers"],
  mixins: [tableMixin],
  computed: {
    portfolioWarrantsTotalAmount() {
      return this.items
        .map((warrant) => warrant.quantite * warrant.prixrevient)
        .reduce((s0, s1) => Number(s0) + Number(s1), 0)
        .toFixed(2);
    },
  },
  methods: {
    sumCol(maturitejours, applyfunction, fixed) {
      return this.items
        .filter((warrant) => warrant.maturitejours == maturitejours)
        .map(applyfunction)
        .reduce((s0, s1) => Number(s0) + Number(s1), 0)
        .toFixed(fixed);
    },
    sumWarrants(maturitejours) {
      var sumWarrants = this.sumCol(maturitejours, (warrant) => warrant.quantite * warrant.prixrevient, 2);
      var totalAmount = this.portfolioWarrantsTotalAmount;
      // return sumWarrants.toString().padStart(8, ' ').replaceAll(' ', '&nbsp;') +
      return sumWarrants + " (" + ((sumWarrants / totalAmount) * 100).toFixed(2) + "%)";
    },
    pvPotentiellesPourcentage(maturitejours) {
      var sumWarrants = this.sumCol(maturitejours, (warrant) => warrant.quantite * warrant.prixrevient, 2);
      var quantite = this.sumCol(maturitejours, (warrant) => warrant.quantite, 0);
      return (((quantite * 10) / sumWarrants - 1) * 100).toFixed(2);
    },
    pvLatentesPourcentage(maturitejours) {
      var sumWarrants = this.sumCol(maturitejours, (warrant) => warrant.quantite * warrant.prixrevient, 2);
      var sumAchats = this.sumCol(maturitejours, (warrant) => warrant.quantite * warrant.achat, 2);
      return ((sumAchats / sumWarrants - 1) * 100).toFixed(2);
    },
    prixDeRevientMoyen(maturitejours) {
      var sumWarrants = this.sumCol(maturitejours, (warrant) => warrant.quantite * warrant.prixrevient, 2);
      var quantite = this.sumCol(maturitejours, (warrant) => warrant.quantite, 0);
      return (sumWarrants / quantite).toFixed(2);
    },
    maturiteJoursOuvrables(maturitejours) {
      var days = maturitejours;
      if (days >= 7) {
        var weeks = Math.floor(maturitejours / 7);
        days = maturitejours - 2 * weeks;
      }
      return days;
    },
  },
  components: {
    "table-stabilitywarrants": httpVueLoader("vuejs/src/components/table-stabilitywarrants.vue"),
  },
};
</script>

<style src="vuejs/src/components/table.css">
</style>
