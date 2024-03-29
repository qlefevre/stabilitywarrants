const { loadModule } = window['vue2-sfc-loader'];
const options = {
    moduleCache: {
        vue: Vue,
    },
    getFile(url) {
        return fetch(url).then(response => {
            if (!response.ok) {
                return Promise.reject(response)
            } else {
                //console.log(url)
                content = response.text()
                content = url.endsWith("-mixin.js") ? { content: content, type: ".mjs" } : content;
                return content;
            }
        });
    },
    addStyle(styleStr) {
        const style = document.createElement('style');
        style.textContent = styleStr;
        const ref = document.head.getElementsByTagName('style')[0] || null;
        document.head.insertBefore(style, ref);
    },
    log(type, ...args) {
        console.log(type, ...args);
    }
}

new Vue({
    el: '#app',
    components: {
        'issuer-filter': () => loadModule('vuejs/src/components/issuer-filter.vue', options),
        'maturity-filter': () => loadModule('vuejs/src/components/maturity-filter.vue', options),
        'pivot-point': () => loadModule('vuejs/src/components/pivot-point.vue', options),
        'isin': () => loadModule('vuejs/src/components/isin.vue', options),
        'table-stabilitywarrants': () => loadModule('vuejs/src/components/table-stabilitywarrants.vue', options),
        'table-portfolio': () => loadModule('vuejs/src/components/table-portfolio.vue', options),
        'links': () => loadModule('vuejs/src/components/links.vue', options)
    },
    vuetify: new Vuetify(),
    data() {
        return {
            filtersousjacent: 'CAC 40',
            filtermaturity: [],
            filterperf: true,
            filtervente: true,
            filterrange: true,
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
                { text: 'Maturité jours', value: 'maturitejours', align: ' hidden-md-and-down' },
                { text: 'Plage', value: 'plage', align: ' hidden-md-and-down' },
                { text: 'Cible', value: 'cible', align: ' hidden-md-and-down' },
                { text: 'Ecart cible abs', value: 'ecartcibleabs', align: ' hidden-md-and-down' },
                { text: 'Perf min %', value: 'perfmin' },
                { text: 'Perf max %', value: 'perfmax' },
                { text: 'Achat', value: 'achat', align: ' hidden-md-and-down' },
                { text: 'Vente', value: 'vente' },
                { text: '+/- % potentielles', value: 'pvpercentage', align: ' hidden-md-and-down' }
            ],
            cfwfiltermaturity: [],
            cfwfiltercapped: true,
            cfwheaders: [
                { text: 'Isin', align: 'start', sortable: false, value: 'isin' },
                { text: 'Type', value: 'cappefloore' },
                { text: 'Prix d\'exercice', value: 'prixexercice' },
                { text: 'Cap', value: 'cap' },
                { text: 'Maturité', value: 'maturite' },
                { text: 'Achat', value: 'achat', align: ' hidden-md-and-down' },
                { text: 'Vente', value: 'vente' }
            ],
            portfolioHeaders: [
                {
                    text: 'Isin',
                    align: 'start',
                    sortable: false,
                    value: 'isin',
                },
                { text: 'Sous-jacent', value: 'sous-jacent' },
                { text: 'Borne basse', value: 'bornebasse', align: ' hidden-md-and-down' },
                { text: 'Borne haute', value: 'bornehaute', align: ' hidden-md-and-down' },
                { text: 'Bornes', value: 'bornes', align: ' hidden-lg-and-up' },
                { text: 'Maturité', value: 'maturite', align: ' hidden-md-and-down', sortable: false },
                { text: 'Maturité jours', value: 'maturitejours' },
                { text: 'Plage', value: 'plage', align: ' hidden-md-and-down' },
                { text: 'Perf min %', value: 'perfmin' },
                { text: 'Perf max %', value: 'perfmax' },
                { text: 'Quantité', value: 'quantite', sortable: false },
                { text: 'Prix de revient', value: 'prixrevient', sortable: false },
                { text: 'Valeur Achat', value: 'achat', sortable: false },
                { text: '+/- latentes', value: 'pvlatentes', sortable: false },
                { text: '+/- % latentes', value: 'pvlatentespercentage', align: ' hidden-md-and-down', sortable: false },
                { text: '+/- potentielles', value: 'pvpotentielles', align: ' hidden-md-and-down', sortable: false },
                { text: '+/- % potentielles', value: 'pvpotentiellespercentage', align: ' hidden-md-and-down', sortable: false },
                { text: 'Action', value: 'actions', align: ' hidden-md-and-down', sortable: false }
            ],
            warrants: [],
            cappedflooreds: [],
            portfolio: [],
            boursoPortfolio: '',
            pivotpoint: {},
            chosenFile: []
        }
    },
    computed: {
        preFilteredWarrants() {
            // émetteurs
            var warrants0 = this.warrants.filter(warrant => this.filterissuers.includes(warrant.issuer));
            // on filtre les valeurs ayant un prix de vente à 10€
            warrants0 = warrants0.filter(warrant => warrant.vente < 10);
            // Sous-jacent
            warrants0 = warrants0.filter(warrant => warrant['sous-jacent'] == this.filtersousjacent);
            // stratégies perf
            if (this.filterperf) {
                warrants0 = warrants0.filter(warrant =>
                    warrant.perfmax > 12 &&
                    warrant.perfmin > 17);
            }
            // stratégies vente
            if (this.filtervente) {
                warrants0 = warrants0.filter(warrant =>
                    warrant.vente < 9.6 && warrant.vente != 0);
            }
            // stratégies plage
            if (this.filterrange) {
                var warrants0Sort = warrants0.sort((a, b) => b.plage - a.plage);
                var bornesMin = [];
                var minPlages = [];
                warrants0Sort.forEach(warrant => {
                    var hash = warrant.maturitejours + '_' + warrant.plage + '_' + warrant.bornebasse;
                    var minHash = warrant.bornebasse + '_' + warrant.maturitejours;
                    if (!bornesMin.includes(minHash)) {
                        minPlages.push(hash);
                        bornesMin.push(minHash);
                    }
                });
                // console.log(bornesMin);
                minPlages.sort();
                // console.log(minPlages);
                warrants0 = warrants0.filter(warrant => {
                    var hash = warrant.maturitejours + '_' + warrant.plage + '_' + warrant.bornebasse;
                    return minPlages.includes(hash);
                });
            }
            return warrants0;
        },
        filteredWarrants() {
            // Applique les filtres en cours
            var warrants0 = this.preFilteredWarrants;
            // Maturité (mois choisi)
            if (this.filtermaturity.length > 0) {
                var patterns = this.filtermaturity.map(month => '/' + month.toString().padStart(2, '0') + '/');
                //console.log('mois: ' + patterns)
                warrants0 = warrants0.filter(warrant => patterns.some(pattern => warrant.maturite.includes(pattern)));
            }
            return warrants0;
        },
        preFilteredCappedFloored() {
            // Cappés ou Floorés
            return this.cappedflooreds.filter(warrant => this.cfwfiltercapped ? warrant.cappefloore == 'Cappés' : warrant.cappefloore == 'Floorés');
        },
        filteredCappedFloored() {
            // Applique les filtres en cours
            var warrants0 = this.preFilteredCappedFloored;
            // Maturité (mois choisi)
            if (this.cfwfiltermaturity.length > 0) {
                var patterns = this.cfwfiltermaturity.map(month => '/' + month.toString().padStart(2, '0') + '/');
                //console.log('mois: ' + patterns)
                warrants0 = warrants0.filter(warrant => patterns.some(pattern => warrant.maturite.includes(pattern)));
            }
            return warrants0;
        },
        portfolioWarrants() {
            // filtrage warrants du portefeuille
            // ajout des infos
            return this.warrants.filter(warrant =>
                this.portfolio.filter(pFVal => warrant.isin.endsWith(pFVal.isin)).length > 0)
                .map(warrant => {
                    warrantPf = Object.assign({}, warrant);
                    pFVal = this.portfolio.filter(pFVal => warrant.isin.endsWith(pFVal.isin))[0];
                    warrantPf.prixrevient = pFVal.prixrevient;
                    warrantPf.quantite = pFVal.quantite;
                    warrantPf.pvlatentes = ((warrantPf.achat - warrantPf.prixrevient) * warrantPf.quantite).toFixed(2);
                    warrantPf.pvlatentespercentage = ((warrantPf.achat / warrantPf.prixrevient - 1) * 100).toFixed(2);
                    warrantPf.pvpotentielles = ((10 - warrantPf.prixrevient) * warrantPf.quantite).toFixed(2);
                    warrantPf.pvpotentiellespercentage = ((10 / warrantPf.prixrevient - 1) * 100).toFixed(2);
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
        },
        portfolioWarrantsTotalAmount() {
            return this.portfolioWarrants.map(warrant => warrant.quantite * warrant.prixrevient)
                .reduce((s0, s1) => Number(s0) + Number(s1), 0).toFixed(2);
        },
        ppArray() {
            array = []
            if (this.isPPLoaded) {
                array = this.pivotpoint[this.filtersousjacent];
                if (array === undefined) {
                    array = [];
                }
            }
            return array;
        },
        isPPLoaded() {
            return Object.keys(this.pivotpoint).length > 0;
        }
    },
    methods: {
        url: function (date, type) {
            var url = undefined;
            switch (type) {
                case 'stabilitywarrants':
                    url = 'https://testqle.s3.nl-ams.scw.cloud/json/%Y/%m/stabilitywarrants-%Y-%m-%d.json';
                    break;
                case 'cappedflooredwarrants':
                    url = 'https://testqle.s3.nl-ams.scw.cloud/json/cf/%Y/%m/cappedflooredwarrants-%Y-%m-%d.json';
                    break;
            }

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
            var portfolio = null;
            // Est-ce une url portfolio=isin-qty-price ?
            var patterns = this.boursoPortfolio.match(/[0-9A-Z]{12}-[0-9]+-[0-9.]+/g);
            if (patterns != null) {
                portfolio = patterns.map(pattern => {
                    var tupleObj = new Object();
                    tupleObj.isin = pattern.substring(0, 12);
                    tupleObj.quantite = Number(pattern.substring(13).match(/[0-9]+/g)[0]);
                    tupleObj.prixrevient = Number(pattern.substring(pattern.lastIndexOf('-') + 1));
                    return tupleObj;
                });
            }
            // Est-ce le contenu de l'export des positions en csv
            var patterns = this.boursoPortfolio.match(/[0-9A-Z]{12};[0-9]+,[0-9]+;[0-9]+,[0-9]+/g);
            if (portfolio == null && patterns != null) {
                portfolio = patterns.map(pattern => {
                    var tupleObj = new Object();
                    tupleObj.isin = pattern.substring(0, 12);
                    tupleObj.quantite = Number(pattern.substring(13, pattern.lastIndexOf(';')).replace(',', '.'));
                    tupleObj.prixrevient = Number(pattern.substring(pattern.lastIndexOf(';') + 1).replace(',', '.'));
                    return tupleObj;
                });
            }
            // Est-ce un copier coller en direct de bourso ?
            var patterns = this.boursoPortfolio.match(/[0-9A-Z]{12}\s+[0-9]+\s+[0-9,]+/g);
            if (portfolio == null && patterns != null) {
                portfolio = patterns.map(pattern => {
                    var tupleObj = new Object();
                    tupleObj.isin = pattern.substring(0, 12);
                    tupleObj.quantite = Number(pattern.substring(12).trimStart().match(/[0-9]+/g)[0]);
                    tupleObj.prixrevient = Number(pattern.substring(pattern.indexOf('\t')).replace(',', '.'));
                    return tupleObj;
                });
            }
            this.portfolio = portfolio;
            console.log('portfolio=' + JSON.stringify(this.portfolio));
        },
        loadPortfolio() {
            // Charge le contenu du fichier dans la zone de texte
            var fr = new FileReader();
            fr.onload = (event) => {
                this.boursoPortfolio = event.target.result;
            }
            fr.readAsText(this.chosenFile);
        },


    },
    mounted() {
        var urlParams = new URLSearchParams(window.location.search);
        // date
        var date = urlParams.get('date') == null ? this.dates[0] : this.parsedate(urlParams.get('date'));
        console.log('date=' + date.string)
        // portfolio
        this.extractPortfolioFromUrl(urlParams.get('portfolio'));

        // télécharge les stability warrants /json/2022/04/stabilitywarrants-2022-04-12.json
        // télécharge les points pivots /json/2022/04/pivotpoint-2022-04-12.json
        var swUrl = this.url(date, 'stabilitywarrants');
        var cfwUrl = this.url(date, 'cappedflooredwarrants');
        var ppUrl = swUrl.replace('stabilitywarrants', 'pivotpoint');
        // fetch pivot point
        fetch(ppUrl)
            .then(response => {
                if (!response.ok) {
                    console.log('Error ' + response.status + ' for ' + ppUrl);
                    return {};
                } else {
                    return response.json();
                }
            })
            .then(data => {
                this.pivotpoint = data
                console.log('pivot point: ' + this.pivotpoint)
            })
        // fetch stabilitywarrants
        fetch(swUrl)
            .then(response => response.json())
            .then(data => {
                this.warrants = data;
                var strmat = this.preFilteredWarrants.map(warrant => warrant.maturite).sort()[0];
                this.filtermaturity = [Number(strmat.substring(strmat.indexOf('/') + 1, strmat.lastIndexOf('/')))];
            });
        // fetch cappedflooredwarrants
        fetch(cfwUrl)
            .then(response => response.json())
            .then(data => {
                this.cappedflooreds = data;
            });
        // stockage local du portefeuille
        if (!this.portfolio.length && localStorage.portfolio) {
            this.portfolio = JSON.parse(localStorage.portfolio);
        }
    },
    watch: {
        // stockage local du portefeuille
        portfolio(newPortfolio) {
            localStorage.portfolio = JSON.stringify(newPortfolio);
        },
        filtersousjacent: function (sousjacent) {
            if (sousjacent !== 'CAC 40') {
                if (!this.filterissuers.includes('UC')) {
                    this.filterissuers.push('UC');
                }
                //console.log(sousjacent);
                //console.log(this.filterissuers);
            }
        }
    }
});
