<template>
  <div class="isin">
    <!-- desktop -->
    <a :href="bourso(this.value)" target="_blank" class="desktop hidden-md-and-down">{{ this.value.isin }}</a>
    <span class="desktop hidden-md-and-down">{{ this.value.mnemo }}</span>
    <!-- mobile -->
    <a :href="bourso(this.value)" target="_blank" class="mobile hidden-lg-and-up">{{ this.value.mnemo }}</a>
    <a :href="bourso(this.value)" target="_blank" class="hidden-md-and-down">
      <v-img
        src="https://www.boursorama.com/bundles/boursoramaui/images/favicons/favicon-16x16.png"
        max-width="16"
        max-height="16"
      >
      </v-img>
    </a>
    <a :href="boursedirect(this.value)" target="_blank" class="hidden-md-and-down">
      <v-img src="https://www.boursedirect.fr/favicon.ico" max-width="16" max-height="16"> </v-img>
    </a>
    <a :href="fortuneo(this.value)" target="_blank" class="hidden-md-and-down" v-if="!this.capped">
      <v-img src="https://bourse.fortuneo.fr/static/assets/img/favicon/favicon.ico" max-width="16" max-height="16">
      </v-img>
    </a>
    <a :href="easybourse(this.value)" target="_blank" class="hidden-md-and-down" v-if="!this.capped">
      <v-img
        src="https://media.easybourse.com/upload/media/image/144000/144081/favicon.jpg"
        max-width="16"
        max-height="16"
      >
      </v-img>
    </a>
    <a v-if="sg(this.value)" :href="sg(this.value)" target="_blank">
      <v-img src="https://sgbourse.fr/favicon.ico" max-width="16" max-height="16"> </v-img>
    </a>
    <a v-if="unicredit(this.value)" :href="unicredit(this.value)" target="_blank">
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
  props: ["value", "capped"],
  methods: {
    bourso: function (item) {
      var prefix = item.issuer == "SG" ? "3rP" : "2rP";
      var suffix = this.capped ? "" : "stability-warrants/";
      return "https://bourse.boursorama.com/bourse/produits-de-bourse/cours/" + suffix + prefix + item.isin;
    },
    boursedirect: function (item) {
      return "https://www.boursedirect.fr/api/search/" + item.isin + "/lucky";
    },
    fortuneo: function (item) {
      var date = item.maturite.substring(3).replace("/20", "");
      var indice = item["sous-jacent"].replace(" ", "").toLowerCase();
      var key = indice + "-" + item.bornebasse + "swt" + date + "t-" + item.mnemo + "-" + item.isin;
      return "https://bourse.fortuneo.fr/certificats/cours-" + key + "-23";
    },
    easybourse: function (item) {
      var date = item.maturite.substring(3).replace("/20", "");
      var indice = item["sous-jacent"].replace(" ", "").toLowerCase();
      var key = indice + "-" + item.bornebasse + "swt" + date + "s/";
      return "https://www.easybourse.com/warrants/" + item.isin + "-25/" + key;
    },
    unicredit: function (item) {
      return item.issuer != "UC" ? "" : "https://www.bourse.unicredit.fr/fr/productpage.html/" + item.isin;
    },
    sg: function (item) {
      return item.issuer != "SG" ? "" : "https://sgbourse.fr/product-details/" + item.mnemo;
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
.isin span.desktop {
  width: 50px;
}
.isin .mobile {
  width: 50px;
}
.isin a,
.isin span {
  padding-right: 5px;
}
</style>