# "RADAR-AS: Reinforcement-Aided Detection and Active Response with Agent-Based Simulation against Disinformation"

## Il modello agent-based

Qui viene presentata la descrizione completa del modello che simula la
diffusione di una fake news all’interno di una rete. La descrizione
segue il protocollo **ODD**. Il modello è stato implementato su NetLogo
6.2.

## Scopo

Il modello simula come una fake news può circolare all’interno di una
rete in cui gli agenti possono avere tre tipi di opinioni: l’opinione A
che supporta la notizia falsa, l’opinione B che è a favore di fatti
veritieri e l’opinione neutra che indica un’indecisione o ignoranza
sull’argomento. Nella simulazione è presente un super agente in grado di
intervenire a ogni passo e decidere quale azione intraprendere per
riuscire a contrastare l’andamento dell’opinione B.

## Entità, variabili di stato, e misure

Il modello include due tipi di entità: i *basic agents* e i *super
agents*. I *basic agents* hanno come variabili: activation treshold,
parametri di network analysis (betweenness, eigenvector, closeness,
clustering, community, page rank, in degree, out degree, degree),
is-a-active, is-b-active, warning, reiterate, is opinion b static,
opinion metric, received A news counter, received b news counter. Il
*super agent* non hanno alcun tipo di attributo visto che il suo scopo è
solo quello di collegarsi ai *basic agents* per compiere le sue
contromisure. La misura dell’ambiente in cui si svolge la simulazione è
dovuto principalmente al numero di agenti presenti all’interno della
rete e dai collegamenti che si creano tra di loro.

## Panoramica del processo e pianificazione

All’inizio della simulazione vengono scelti il numero di nodi da cui
deve essere composta la rete, il numero di *tick* che determinano la
durata della simulazione e il tipo di rete che si vuole costruire, che
può essere di tipo: *Erdős–Rényi*, *Small World* e *Preferencial
Attachment*. In base al tipo di rete scelta si impostano i parametri
della creazione dei collegamenti fra i nodi. Nel caso di una rete
*Erdős–Rényi*, viene impostato un paramtro *k* che determina il valore
di distribuzione normale con cui vengono generati il numero collegamenti
che devono avere i nodi insieme alla deviazione standard. Per la rete di
tipo *Small World*, vengono selezionate la *Neighborhood Size* e la
*Rewire Probability*, che corrispondono rispettivamente al numero di
nodi a cui deve essere collegato un nodo e alla probabilità che ciascun
arco sia disconnesso da una delle sue estremità e connesso a un altro
nodo nella rete scelto a caso. Infine per il *Preferencial Attachment*
viene gererata una network di tipo "scale free", in cui gli agenti sono
aggiunti, uno alla volta, ciascuno formando collegamenti pari al numero
minimo di link (uno nel nostro caso) con i nodi aggiunti
precedentemente. Più collegamenti ha un nodo, maggiore è la possibilità
che i nuovi nodi creino dei collegamenti con esso quando sono
aggiunti.  
### Echo Chamber
Una volta creata la rete viene inizializzata la di cui fanno parte i
nodi che sostengono l’opinione della fake news. La vien vista come un
insieme di utenti caratterizzata da due proprietà: l’opinion polarization e la network polarization. 
L’ opinion polarizationimplicache gli utenti, in relazione a un’opinione, sono più inclini a
condividerne le vedute. La network polarization indica che gli utenti sono più connessi gli
uni con gli altri rispetto al resto della network. In altre parole, una
ha dei nodi più strettamente connessi che tendono a condividere la
stessa opinione su una determinata narrativa. Vengono quindi impostati i
valori di Po e Pn, e per la creazione della viene scelta
anche la frazione dei nodi che ne devono far parte, tramite il parametro
echo chamber fraction. All’inizio della creazione, viene moltiplicata la per il numero di
nodi, così da ottenere il numero di nodi che devono essere inseriti
nella. Il calcolo per ottenere il numero di archi è E=N/2, dove N è
il numero di nodi e K è il grado medio che hanno i nodi, impostato
all’inizio della simulazione. Il grado medio viene diviso per due, visto
che i collegamenti non sono direzionati e ogni arco ha due lati.
Successivamente il valore ottenuto viene moltiplicato per Pn.
L’equazione finale sarà:
E = N * Pn
Il valore *E*, serve a determinare quanti archi devono essere scelti
dall’insieme totale degli archi della rete. Su tutti gli archi scelti,
in modo casuale, viene eseguito un controllo per verificare se
esattamente un nodo, appartenente a una delle due estremità, appartiene
alla . Se così l’arco viene eliminato e viene sostituito con un
collegamento tra il nodo che già faceva parte dell’ e un altro che ne
faccia parte. Così facendo aumenta il grado di tra i nodi appartenenti
alla , creando più coesione. Successivamente, viene scelto un nodo
casuale che fa parte della , cher serve come punto di attivazione, in
quanto a questo viene impostato l’opinione di tipo A (attribuendo anche
un valore casuale dell’ che rientri in quelli relativi all’opinione) e
con esso tutti i nodi collegati a quest’ultimo. La stessa procedura di
attivazione viene ripetuta anche per i nodi di tipo B, dove viene scelto
un nodo all’esterno della , che viene impostato come attivo verso
l’opinione B e tutti i nodi a esso collegati, che non abbiano già
un’opinione di tipo A e che non facciano parte della . Una volta
terminata questa procedura, viene impostata la soglia di attivazione a
ciascuno dei nodi della rete; in particolare ai nodi appartenenti alla ,
viene impostato un *Θ* pari a *Θ* − *P**o*, mentre ai nodi al di fuori
viene impostato semplicemente il valore di *Θ*, scelto all’inzio della
simulazione.
### Super agente
Dopo aver creato la rete e costruita la *echo chamber*,
viene inserito il super agente all’interno della rete. Questo tipo di
agente non ha attributi e ha a disposizione tre azioni che hanno lo
scopo di contrastare l’andamento dell’opinione A durante la simulazione
e ridurre la *global cascade*, corrispondente alla frazione dei nodi
attivi di tipo A. Le azioni sono: *warning*, *reiterate* e *static b
nodes*. Durante il posizionamento del super agente, questo viene
collegato a un numero di nodi specificato dal parametro *node-range* e
il criterio con cui vengono selezionati i nodi è il seguente: vengono
scelti i nodi con *betweenness*, *page rank* o *degree* più alti. I
calcoli vengono eseguiti ad ogni passo della simulazione per creare i
collegamenti, visto che i valori possono cambiare nel corso del tempo.
Inoltre, se il super agente aveva già dei collegamenti, questi vengono
eliminati per essere sostituiti con quelli nuovi.  
### Go
Dopo aver inizializzato la rete, può iniziare la simulazione. Il
modello procede in istanti di tempo determinati dai *tick*. All’inizio
vengono controllate se è stata attivata una delle tre azioni, ed
eseguendo un ulteriore controllo per evitare di attivare più azioni allo
stesso *tick*. Se un agente ha cambiato la sua opinione in un
determinato *tick*, questo verrà impostato come attivo verso l’opinione
A o B solo al passo successivo. Successivamente viene chiesto a tutti i
*basic agents* di contare il numero di nodi vicini di tipo A o B e
calcolarne la frazione. In base al tipo di frazione predominante viene
fatto il confronto di quest’ultima con la treshold. Se la frazione è
maggiore della soglia di attivazione *Θ*, viene calcolata l’*opinion
metric*. Se le frazioni di tipo A e B sono uguali, viene fatta una
scelta casuale sull’opinione che influenzerà l’agente. Dopo aver
eseguito la procedura principale di diffusione delle notizie, entrano in
atto le azioni del super agente, se attive. Alla fine della simulazione,
una volta raggiunto il numero di *tick* stabilito, viene calcolata la
*global cascade*.

## Sotto-modelli

In questa sottosezione verranno analizzate le azioni che può compiere il
super agente e l’*opinion metric*.

### Warning

Il *Warning* ha effetto solo sui nodi di tipo A o neutrali e può essere
di tue tipo: globale o non globale. Se il *Warning* è globale, quando
viene attivato, viene impostata la variabile *warning* a *true* di tutti
gli agenti della rete. Se il *Warning* non è globale, il super agente
manda il segnale di *warning* solo agli agenti a cui è collegato.
Inoltre, sono presenti due parametri che regolano l’influenza del
*Warning*: uno per i nodi con l’opinione di tipo A e uno per i nodi
neutrali. Questo perché se un nodo non ha un’opinione è più probabile
che il *Warning* abbia un effetto maggiore su di esso e viceversa per i
nodi che già ne hanno una. Dopo che un nodo ha ricevuto un’opinione,
controlla se la sua variabile di *warning* è impostata a *true*. Se
così, viene generato un numero casuale tra 0 e 1 e viene verificato che
questo valore sia minore o uguale della soglia del *warning impact*
impostata all’inizio della simulazione. Nel caso in cui il numero
generato sia minore viene avviata la procedura di calcolo dell’*opinion
metric*.

### Reiterate

La procedura di *Reiterate* avviata dal super agente imposta a *true* la
variabile corrispettiva che è presente sui nodi ad esso collegati. Dopo
che un nodo ha ricevuto un’opinione controlla lo stato della variabile
*reiterate*. I nodi con questa variabile attiva riceveranno un’altra
notizia di tipo b ad ogni *tick* successivo per un numero di volte pari
a quanti collegamenti quel nodo ha. Per esempio, se un nodo ha dieci
collegamenti, per dieci *tick* riceverà un’opinione di tipo B, ripetendo
il controllo sulla soglia di attivazione. A differenza della diffusione
normale, in cui viene analizzata la frazione dei nodi di tipo A o B, in
questo caso verrà generato un numero casuale tra 0 e 1 e viene fatto un
controllo per vedere se il valore è minore o uguale del *Θ* del nodo.
L’operazione di reiterate può anche finire prima se il nodo cambia
opinione prima che raggiunga il numero massimo di iterazioni stabilite.

### Static B Agents

L’azione *Static B agents* permette al super agente di forzare alcuni
nodi, scelti con tre criteri diversi, di mantenere l’opinione B fino
alla fine della simulazione. Quindi questi anche se ricevessero notizie
di tipo A, queste non influenzerebbero questi nodi. Vengono scelti i
nodi con *betweenness*, *page rank* o *degree* più alti. Il numero di
nodi scelto è selezionato dal parametro *node range*. Quello che
sostanzialmente fa il super agente è impostare l’*opinion metric* a 0 e
imosta a *true* una variabile presente sugli agenti chiamata
*is-opinion-b-static*. Così, durante la simulazione viene controllata se
questa variabile è attiva così da non far cambiare opinione al nodo.

### Opinion metric

Ogni nodo ha un’*opinion metric* che può assumere valori da 0 a 1 e, in
particolare:

-   se il valore è compreso tra 0 e 0.33, l’agente ha un opinione di
    tipo B

-   se il valore è compreso tra 0.34 e 0.65, l’agente non ha un
    opinione, quindi è neutro

-   se il valore è comrpreso tra 0.66 e 1, l’agente ha un opinione di
    tipo A

Inoltre, all’inzio della simulazione viene scelto di quanto deve
cambiare l’*opinion metric* quando l’agente riceve un opinione e supera
la sua soglia di attivazione, tramite l’*opinion metric step*.
