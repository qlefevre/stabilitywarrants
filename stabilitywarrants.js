new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data() {
    return {
      filtersousjacent: 'CAC 40',
      filtermaturitydays: [30],
      filterperf: true,
      filterissuers: ['SG','UC'],
      headers: [
        {
          text: 'Isin',
          align: 'start',
          sortable: false,
          value: 'isin',
        },
        {
          text: 'Sous-jacent', value: 'sous-jacent',
          filter: value => {
            if (!this.filtersousjacent) return true
            return this.filtersousjacent == value
          }
        },
        { text: 'Borne basse', value: 'borne basse' },
        { text: 'Borne haute', value: 'borne haute' },
        { text: 'Maturité', value: 'maturite' },
        { text: 'Maturité jours', value: 'maturite jours' },
        { text: 'Plage', value: 'plage' },
        { text: 'Cible', value: 'cible' },
        { text: 'Ecart cible abs', value: 'ecart cible abs' },
        { text: 'Perf min %', value: 'perf min' },
        { text: 'Perf max %', value: 'perf max' }
      ],
      maturitydays: [30,60,90],
      issuers: [{key:'SG',name:'Société Générale'},{key:'UC',name:'Unicredit'}],
      warrants: [],
    }
  },
  computed: {
    filteredWarrants() {
      var warrants0 = this.warrants;
      // émetteurs
      warrants0 = warrants0.filter(warrant => this.filterissuers.includes(warrant['issuer']));
      // stratégies perf
      if (this.filterperf) {
        warrants0 = warrants0.filter(warrant =>
          warrant['perf max'] > 8 &&
          warrant['perf min'] > 15 &&
          warrant['perf min'] > warrant['perf max']);
      }
        // Maturité jours
        var minVal = Math.min.apply(Math, this.filtermaturitydays)-30;
        var maxVal = Math.max.apply(Math,this.filtermaturitydays);
        //console.log('min '+minVal+' max '+maxVal)
        warrants0 = warrants0.filter(warrant =>
         minVal < warrant['maturite jours'] && warrant['maturite jours'] < maxVal);

      return warrants0;
    },
    sousjacents() {
      var sousjacents0 = this.filteredWarrants.map(warrant => warrant['sous-jacent']);
      sousjacents0 = sousjacents0.filter((x, i, a) => a.indexOf(x) == i);
      sousjacents0.unshift('');
      return sousjacents0;
    }
  },
  methods: {
    bourso: function (item) {
      var prefix = item.issuer == 'SG' ? '3rP' : '2rP';
      return 'https://www.boursorama.com/bourse/produits-de-bourse/cours/stability-warrants/' + prefix + item.isin
    }
  },
  mounted() {
    var url = 'https://testqle.s3.nl-ams.scw.cloud/json/%Y/%m/stabilitywarrants-%Y-%m-%d.json';
    var now = new Date();
    url = url.replaceAll('%Y', now.getYear() + 1900);
    url = url.replaceAll('%m', String(now.getMonth() + 1).padStart(2, '0'));
    url = url.replaceAll('%d', String(now.getDate()).padStart(2, '0'));

    fetch(url)
      .then(response => response.json())
      .then(data => {
        this.warrants = data;
      });
  }
})