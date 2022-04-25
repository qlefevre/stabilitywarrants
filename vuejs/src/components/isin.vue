<template>
  <div class="isin">
    <!-- desktop -->
    <a
      :href="bourso(this.value)"
      target="_blank"
      class="desktop hidden-md-and-down"
      >{{ this.value.isin }}</a
    >
    <!-- mobile -->
    <a
      :href="bourso(this.value)"
      target="_blank"
      class="mobile hidden-lg-and-up"
      >{{ this.value.mnemo }}</a
    >
    <a :href="bourso(this.value)" target="_blank" class="hidden-md-and-down">
      <v-img
        src="https://www.boursorama.com/bundles/boursoramaui/images/favicons/favicon-16x16.png"
        max-width="16"
        max-height="16"
      >
      </v-img>
    </a>
    <a
      :href="boursedirect(this.value)"
      target="_blank"
      class="hidden-md-and-down"
    >
      <v-img
        src="https://www.boursedirect.fr/favicon.ico"
        max-width="16"
        max-height="16"
      >
      </v-img>
    </a>
    <a v-if="sg(this.value)" :href="sg(this.value)" target="_blank">
      <v-img
        src="https://sgbourse.fr/favicon.ico"
        max-width="16"
        max-height="16"
      >
      </v-img>
    </a>
    <a
      v-if="unicredit(this.value)"
      :href="unicredit(this.value)"
      target="_blank"
    >
      <v-img
        src="https://www.bourse.unicredit.fr/etc/designs/onemarkets-relaunch/favicon.ico"
        max-width="16"
        max-height="16"
      >
      </v-img>
    </a>
  </div>
</template>

<script>
module.exports = {
  props: ["value"],
  methods: {
    bourso: function (item) {
      var prefix = item.issuer == "SG" ? "3rP" : "2rP";
      return (
        "https://www.boursorama.com/bourse/produits-de-bourse/cours/stability-warrants/" +
        prefix +
        item.isin
      );
    },
    boursedirect: function (item) {
      return "https://www.boursedirect.fr/api/search/" + item.isin + "/lucky";
    },
    unicredit: function (item) {
      return item.issuer != "UC"
        ? ""
        : "https://www.bourse.unicredit.fr/fr/productpage.html/" + item.isin;
    },
    sg: function (item) {
      return item.issuer != "SG"
        ? ""
        : "https://sgbourse.fr/product-details/" + item.mnemo;
    },
  },
};
</script>

<style>
.isin {
  display: flex;
  vertical-align: middle;
}
.isin .desktop {
  width: 110px;
}
.isin .mobile {
  width: 50px;
}
.isin a {
  padding-right: 5px;
}
</style>