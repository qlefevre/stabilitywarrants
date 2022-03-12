new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data() {
        return {
            filtersousjacent: 'CAC 40',
            filtermaturitydays: [30],
            filterperf: true,
            filterissuers: ['SG'],
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
                        if (!this.filtersousjacent) {
                            return true
                        }
                        return this.filtersousjacent == value
                    }
                },
                { text: 'Borne basse', value: 'bornebasse' },
                { text: 'Borne haute', value: 'bornehaute' },
                { text: 'Maturité', value: 'maturite' },
                { text: 'Maturité jours', value: 'maturitejours' },
                { text: 'Plage', value: 'plage' },
                { text: 'Cible', value: 'cible' },
                { text: 'Ecart cible abs', value: 'ecartcibleabs' },
                { text: 'Perf min %', value: 'perfmin' },
                { text: 'Perf max %', value: 'perfmax' }
            ],
            portfolioHeaders: [
                {
                    text: 'Isin',
                    align: 'start',
                    sortable: false,
                    value: 'isin',
                },
                { text: 'Sous-jacent', value: 'sous-jacent' },
                { text: 'Borne basse', value: 'bornebasse' },
                { text: 'Borne haute', value: 'bornehaute' },
                { text: 'Maturité', value: 'maturite' },
                { text: 'Maturité jours', value: 'maturitejours' },
                { text: 'Plage', value: 'plage' },
                { text: 'Perf min %', value: 'perfmin' },
                { text: 'Perf max %', value: 'perfmax' },
                { text: 'Quantité', value: 'quantite' },
                { text: 'Prix de revient', value: 'prixrevient' },
                { text: 'Valeur Achat', value: 'achat' },
                { text: '+/- latentes', value: 'pvlatentes' },
                { text: '+/- potentielles %', value: '+/-potentielles' },
                { text: '+/- potentielles', value: 'pvpotentielles' },
            ],
            maturitydays: [30, 60, 90, 120, 150],
            issuers: [{ key: 'SG', name: 'Société Générale' }, { key: 'UC', name: 'Unicredit' }],
            warrants: [],
            portfolio: [],
            boursoPortfolio: '',
            pivotpoint: { "S3": 5601.19, "S2": 6017.04, "S1": 6337.93, "P": 6753.78, "R1": 7074.67, "R2": 7490.52, "R3": 7811.41 }
        }
    },
    computed: {
        filteredWarrants() {
            // émetteurs
            var warrants0 = this.warrants.filter(warrant => this.filterissuers.includes(warrant['issuer']));
            // stratégies perf
            if (this.filterperf) {
                warrants0 = warrants0.filter(warrant =>
                    warrant['perfmax'] > 8 &&
                    warrant['perfmin'] > 15 &&
                    warrant['perfmin'] > warrant['perfmax']);
            }
            // Maturité jours
            var minVal = Math.min.apply(Math, this.filtermaturitydays) - 30;
            var maxVal = Math.max.apply(Math, this.filtermaturitydays);
            //console.log('min '+minVal+' max '+maxVal)
            warrants0 = warrants0.filter(warrant =>
                minVal < warrant['maturitejours'] && warrant['maturitejours'] < maxVal);

            return warrants0;
        },
        portfolioWarrants() {
            // filtrage warrants du portefeuille
            // ajout des infos
            return this.warrants.filter(warrant =>
                this.portfolio.filter(pFVal => warrant['isin'].endsWith(pFVal.isin)).length > 0)
                .map(warrant => {
                    warrantPf = Object.assign({}, warrant);
                    pFVal = this.portfolio.filter(pFVal => warrant['isin'].endsWith(pFVal.isin))[0];
                    warrantPf.prixrevient = pFVal.prixrevient;
                    warrantPf.quantite = pFVal.quantite;
                    warrantPf.pvlatentes = ((warrantPf.achat - warrantPf.prixrevient) * warrantPf.quantite).toFixed(2);
                    warrantPf.pvpotentielles = ((10 - warrantPf.prixrevient) * warrantPf.quantite).toFixed(2);
                    return warrantPf;
                });

        },
        capitalGains() {
            var capitalGains = new Object();
            const pFWs = this.portfolioWarrants;
            const sum = (s0, s1) => Number(s0) + Number(s1)
            capitalGains.pvlatentes = pFWs.length == 0 ? 0 : pFWs.map(w => w.pvlatentes)
                .reduce(sum, 0).toFixed(2);
            capitalGains.pvpotentielles = pFWs.length == 0 ? 0 : pFWs.map(w => w.pvpotentielles)
                .reduce(sum, 0).toFixed(2);
            return capitalGains;
        },
        sousjacents() {
            var sousjacents0 = this.filteredWarrants.map(warrant => warrant['sous-jacent']);
            sousjacents0 = sousjacents0.filter((x, i, a) => a.indexOf(x) == i);
            sousjacents0.unshift('');
            return sousjacents0;
        },
        dates() {
            var now = new Date();
            var dates = [];
            for (var i = 0; i < 7; i++) {
                var date = {
                    year: now.getYear() + 1900,
                    month: String(now.getMonth() + 1).padStart(2, '0'),
                    date: String(now.getDate()).padStart(2, '0')
                }
                date.string = date.year + '-' + date.month + '-' + date.date;
                dates.push(date);
                now.setDate(now.getDate() - 1);
            }
            console.log(dates);
            return dates;
        }
    },
    methods: {
        bourso: function (item) {
            var prefix = item.issuer == 'SG' ? '3rP' : '2rP';
            return 'https://www.boursorama.com/bourse/produits-de-bourse/cours/stability-warrants/' + prefix + item.isin
        },
        url: function (date) {
            var url = 'https://testqle.s3.nl-ams.scw.cloud/json/%Y/%m/stabilitywarrants-%Y-%m-%d.json';
            url = url.replaceAll('%Y', date.year);
            url = url.replaceAll('%m', date.month);
            url = url.replaceAll('%d', date.date);
            return url;
        },
        parsedate: function (str) {
            var parts = str.split('-');
            date = {
                year: parts[0],
                month: parts[1],
                date: parts[2],
            };
            date.string = date.year + '-' + date.month + '-' + date.date;
            return date;

        },
        portfoliocodes: function (short) {
            return this.portfolioWarrants.map(warrant =>
                warrant.isin + '-' + warrant.quantite + '-' + warrant.prixrevient)
                .map(isin => short ? isin.substring(7) : isin).join();
        },
        getPerfStyle(perf) {
            if (perf < 7) return 'color:red;font-weight:bold;'
            else if (perf < 12) return 'color:orange;font-weight:bold;'
            else return ''
        },
        getPvStyle(pv) {
            if (pv < 0) return 'color:red;'
            return 'color:forestgreen;'
        },
        extractPortfolioFromUrl(portfolioparam) {
            if (portfolioparam == undefined || portfolioparam == null)
                this.portfolio = [];
            else
                this.portfolio = portfolioparam.split(',').map(tuple => {
                    var values = tuple.split('-');
                    var tupleObj = new Object();
                    tupleObj.isin = values[0];
                    tupleObj.quantite = values[1] == undefined ? 0 : Number(values[1]);
                    tupleObj.prixrevient = values[2] == undefined ? 0 : Number(values[2]);
                    return tupleObj;
                });
            console.log('portfolio=' + JSON.stringify(this.portfolio));
        },
        extractPortfolioFromText() {
            var patterns = this.boursoPortfolio.match(/[0-9A-Z]{12}\s+[0-9]+\s+[0-9,]+/g);
            this.portfolio = patterns.map(pattern => {
                var tupleObj = new Object();
                tupleObj.isin = pattern.substring(0, 12);
                tupleObj.quantite = Number(pattern.substring(12).trimStart().match(/[0-9]+/g)[0]);
                tupleObj.prixrevient = Number(pattern.substring(pattern.indexOf('\t')).replace(',', '.'));
                return tupleObj;
            });
            console.log('portfolio=' + JSON.stringify(this.portfolio));
        },
        disabledIssuer(issuer) {
            return this.warrants.filter(warrant => issuer == warrant['issuer']).length == 0;
        },
        sumPvlatentes(maturitejours) {
            return this.portfolioWarrants.filter(warrant => warrant.maturitejours == maturitejours)
                .map(warrant => warrant.pvlatentes)
                .reduce((s0, s1) => Number(s0) + Number(s1), 0).toFixed(2);
        },
        sumPvpotentielles(maturitejours) {
            return this.portfolioWarrants.filter(warrant => warrant.maturitejours == maturitejours)
                .map(warrant => warrant.pvpotentielles)
                .reduce((s0, s1) => Number(s0) + Number(s1), 0).toFixed(2);
        }
    },
    mounted() {
        var urlParams = new URLSearchParams(window.location.search);
        // date
        var date = urlParams.get('date') == null ? this.dates[0] : this.parsedate(urlParams.get('date'));
        console.log('date=' + date.string)
        // portfolio
        this.extractPortfolioFromUrl(urlParams.get('portfolio'));

        // retrieve stability warrants
        var url = this.url(date);
        fetch(url)
            .then(response => response.json())
            .then(data => {
                this.warrants = data;
            });
    }
})
