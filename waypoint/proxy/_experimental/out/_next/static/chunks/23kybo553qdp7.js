(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,871943,502547,e=>{"use strict";var t=e.i(271645);let r=t.forwardRef(function(e,r){return t.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:r},e),t.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M19 9l-7 7-7-7"}))});e.s(["ChevronDownIcon",0,r],871943);let n=t.forwardRef(function(e,r){return t.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:r},e),t.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M9 5l7 7-7 7"}))});e.s(["ChevronRightIcon",0,n],502547)},360820,e=>{"use strict";var t=e.i(271645);let r=t.forwardRef(function(e,r){return t.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:r},e),t.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M5 15l7-7 7 7"}))});e.s(["ChevronUpIcon",0,r],360820)},434626,e=>{"use strict";var t=e.i(271645);let r=t.forwardRef(function(e,r){return t.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:r},e),t.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"}))});e.s(["ExternalLinkIcon",0,r],434626)},250980,e=>{"use strict";var t=e.i(271645);let r=t.forwardRef(function(e,r){return t.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:r},e),t.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"}))});e.s(["PlusCircleIcon",0,r],250980)},278587,e=>{"use strict";var t=e.i(271645);let r=t.forwardRef(function(e,r){return t.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:r},e),t.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"}))});e.s(["RefreshIcon",0,r],278587)},68155,e=>{"use strict";var t=e.i(271645);let r=t.forwardRef(function(e,r){return t.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:r},e),t.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"}))});e.s(["TrashIcon",0,r],68155)},655063,e=>{"use strict";var t=e.i(540626),r=e.i(271645);e.s(["useDebouncedValue",0,function(e,n,o){let[i,s,a]=function(e,n,o){let[i,s]=(0,r.useState)(e),a=(0,t.useDebouncer)(s,n,o);return[i,a.maybeExecute,a]}(e,n,o);return(0,r.useEffect)(()=>{s(e)},[e,s]),[i,a]}],655063)},540626,e=>{"use strict";let t;var r=e.i(271645);let n=(0,r.createContext)(null);function o(e,t){if(Object.is(e,t))return!0;if("object"!=typeof e||null===e||"object"!=typeof t||null===t)return!1;if(e instanceof Map&&t instanceof Map){if(e.size!==t.size)return!1;for(let[r,n]of e)if(!t.has(r)||!Object.is(n,t.get(r)))return!1;return!0}if(e instanceof Set&&t instanceof Set){if(e.size!==t.size)return!1;for(let r of e)if(!t.has(r))return!1;return!0}if(e instanceof Date&&t instanceof Date)return e.getTime()===t.getTime();let r=i(e);if(r.length!==i(t).length)return!1;for(let n=0;n<r.length;n++)if(!Object.prototype.hasOwnProperty.call(t,r[n])||!Object.is(e[r[n]],t[r[n]]))return!1;return!0}function i(e){return Object.keys(e).concat(Object.getOwnPropertySymbols(e))}var s=e.i(430224);function a(e,t){return e===t}function l(e,t=e=>e,n){let o=n?.compare??a,i=(0,r.useCallback)(t=>{let{unsubscribe:r}=e.subscribe(t);return r},[e]),u=(0,r.useCallback)(()=>e.get(),[e]);return(0,s.useSyncExternalStoreWithSelector)(i,u,u,t,o)}function u(e,...t){return"function"==typeof e?e(...t):e}var c=class{#e=!0;#t;#r;#n;#o;#i;#s;#a;#l=0;#u=5;#c=!1;#d=!1;#p=null;#h=()=>{this.debugLog("Connected to event bus"),this.#i=!0,this.#c=!1,this.debugLog("Emitting queued events",this.#o),this.#o.forEach(e=>this.emitEventToBus(e)),this.#o=[],this.stopConnectLoop(),this.#r().removeEventListener("tanstack-connect-success",this.#h)};#g=()=>{if(this.#l<this.#u){this.#l++,this.dispatchCustomEvent("tanstack-connect",{});return}this.#r().removeEventListener("tanstack-connect",this.#g),this.#d=!0,this.debugLog("Max retries reached, giving up on connection"),this.stopConnectLoop()};#m=()=>{this.#c||(this.#c=!0,this.#r().addEventListener("tanstack-connect-success",this.#h),this.#g())};constructor({pluginId:e,debug:t=!1,enabled:r=!0,reconnectEveryMs:n=300}){this.#t=e,this.#e=r,this.#r=this.getGlobalTarget,this.#n=t,this.debugLog(" Initializing event subscription for plugin",this.#t),this.#o=[],this.#i=!1,this.#d=!1,this.#s=null,this.#a=n}startConnectLoop(){null!==this.#s||this.#i||(this.debugLog(`Starting connect loop (every ${this.#a}ms)`),this.#s=setInterval(this.#g,this.#a))}stopConnectLoop(){this.#c=!1,null!==this.#s&&(clearInterval(this.#s),this.#s=null,this.#o=[],this.debugLog("Stopped connect loop"))}debugLog(...e){this.#n&&console.log(`🌴 [tanstack-devtools:${this.#t}-plugin]`,...e)}getGlobalTarget(){if("u">typeof globalThis&&globalThis.__TANSTACK_EVENT_TARGET__)return this.debugLog("Using global event target"),globalThis.__TANSTACK_EVENT_TARGET__;if("u">typeof window&&void 0!==window.addEventListener)return this.debugLog("Using window as event target"),window;let e="u">typeof EventTarget?new EventTarget:void 0;return void 0===e||void 0===e.addEventListener?(this.debugLog("No event mechanism available, running in non-web environment"),{addEventListener:()=>{},removeEventListener:()=>{},dispatchEvent:()=>!1}):(this.debugLog("Using new EventTarget as fallback"),e)}getPluginId(){return this.#t}dispatchCustomEventShim(e,t){try{let r=new Event(e,{detail:t});this.#r().dispatchEvent(r)}catch(e){this.debugLog("Failed to dispatch shim event")}}dispatchCustomEvent(e,t){try{this.#r().dispatchEvent(new CustomEvent(e,{detail:t}))}catch(r){this.dispatchCustomEventShim(e,t)}}emitEventToBus(e){this.debugLog("Emitting event to client bus",e),this.dispatchCustomEvent("tanstack-dispatch-event",e)}createEventPayload(e,t){return{type:`${this.#t}:${e}`,payload:t,pluginId:this.#t}}emit(e,t){if(!this.#e)return void this.debugLog("Event bus client is disabled, not emitting event",e,t);if(this.#p&&(this.debugLog("Emitting event to internal event target",e,t),this.#p.dispatchEvent(new CustomEvent(`${this.#t}:${e}`,{detail:this.createEventPayload(e,t)}))),this.#d)return void this.debugLog("Previously failed to connect, not emitting to bus");if(!this.#i){this.debugLog("Bus not available, will be pushed as soon as connected"),this.#o.push(this.createEventPayload(e,t)),"u">typeof CustomEvent&&!this.#c&&(this.#m(),this.startConnectLoop());return}return this.emitEventToBus(this.createEventPayload(e,t))}on(e,t,r){let n=r?.withEventTarget??!1,o=`${this.#t}:${e}`;if(n&&(this.#p||(this.#p=new EventTarget),this.#p.addEventListener(o,e=>{t(e.detail)})),!this.#e)return this.debugLog("Event bus client is disabled, not registering event",o),()=>{};let i=e=>{this.debugLog("Received event from bus",e.detail),t(e.detail)};return this.#r().addEventListener(o,i),this.debugLog("Registered event to bus",o),()=>{n&&this.#p?.removeEventListener(o,i),this.#r().removeEventListener(o,i)}}onAll(e){if(!this.#e)return this.debugLog("Event bus client is disabled, not registering event"),()=>{};let t=t=>{e(t.detail)};return this.#r().addEventListener("tanstack-devtools-global",t),()=>this.#r().removeEventListener("tanstack-devtools-global",t)}onAllPluginEvents(e){if(!this.#e)return this.debugLog("Event bus client is disabled, not registering event"),()=>{};let t=t=>{let r=t.detail;this.#t&&r.pluginId!==this.#t||e(r)};return this.#r().addEventListener("tanstack-devtools-global",t),()=>this.#r().removeEventListener("tanstack-devtools-global",t)}};let d=new Map;function p(e){if(void 0!==e)try{return JSON.parse(JSON.stringify(e))}catch{return null}}let h=new class extends c{constructor(e){super({pluginId:"pacer",debug:e?.debug,reconnectEveryMs:1e3})}};function g(e,t,r){let n="object"==typeof e,o=n?e:void 0;return{next:(n?e.next:e)?.bind(o),error:(n?e.error:t)?.bind(o),complete:(n?e.complete:r)?.bind(o)}}let m=[],b=0,{link:f,unlink:v,propagate:x,checkDirty:k,shallowPropagate:_}=function({update:e,notify:t,unwatched:r}){return{link:function(e,t,r){let n=t.depsTail;if(void 0!==n&&n.dep===e)return;let o=void 0!==n?n.nextDep:t.deps;if(void 0!==o&&o.dep===e){o.version=r,t.depsTail=o;return}let i=e.subsTail;if(void 0!==i&&i.version===r&&i.sub===t)return;let s=t.depsTail=e.subsTail={version:r,dep:e,sub:t,prevDep:n,nextDep:o,prevSub:i,nextSub:void 0};void 0!==o&&(o.prevDep=s),void 0!==n?n.nextDep=s:t.deps=s,void 0!==i?i.nextSub=s:e.subs=s},unlink:function(e,t=e.sub){let n=e.dep,o=e.prevDep,i=e.nextDep,s=e.nextSub,a=e.prevSub;return void 0!==i?i.prevDep=o:t.depsTail=o,void 0!==o?o.nextDep=i:t.deps=i,void 0!==s?s.prevSub=a:n.subsTail=a,void 0!==a?a.nextSub=s:void 0===(n.subs=s)&&r(n),i},propagate:function(e){let r,n=e.nextSub;e:for(;;){let o=e.sub,i=o.flags;if(60&i?12&i?4&i?!(48&i)&&function(e,t){let r=t.depsTail;for(;void 0!==r;){if(r===e)return!0;r=r.prevDep}return!1}(e,o)?(o.flags=40|i,i&=1):i=0:o.flags=-9&i|32:i=0:o.flags=32|i,2&i&&t(o),1&i){let t=o.subs;if(void 0!==t){let o=(e=t).nextSub;void 0!==o&&(r={value:n,prev:r},n=o);continue}}if(void 0!==(e=n)){n=e.nextSub;continue}for(;void 0!==r;)if(e=r.value,r=r.prev,void 0!==e){n=e.nextSub;continue e}break}},checkDirty:function(t,r){let o,i=0,s=!1;e:for(;;){let a=t.dep,l=a.flags;if(16&r.flags)s=!0;else if((17&l)==17){if(e(a)){let e=a.subs;void 0!==e.nextSub&&n(e),s=!0}}else if((33&l)==33){(void 0!==t.nextSub||void 0!==t.prevSub)&&(o={value:t,prev:o}),t=a.deps,r=a,++i;continue}if(!s){let e=t.nextDep;if(void 0!==e){t=e;continue}}for(;i--;){let i=r.subs,a=void 0!==i.nextSub;if(a?(t=o.value,o=o.prev):t=i,s){if(e(r)){a&&n(i),r=t.sub;continue}s=!1}else r.flags&=-33;r=t.sub;let l=t.nextDep;if(void 0!==l){t=l;continue e}}return s}},shallowPropagate:n};function n(e){do{let r=e.sub,n=r.flags;(48&n)==32&&(r.flags=16|n,(6&n)==2&&t(r))}while(void 0!==(e=e.nextSub))}}({update:e=>e._update(),notify(e){m[w++]=e,e.flags&=-3},unwatched(e){void 0!==e.depsTail&&(e.depsTail=void 0,e.flags=17,E(e))}}),y=0,w=0;function E(e){let t=e.depsTail,r=void 0!==t?t.nextDep:e.deps;for(;void 0!==r;)r=v(r,e)}var C=class{constructor(e,r){this.atom=function(e){let r="function"==typeof e,n={_snapshot:r?void 0:e,subs:void 0,subsTail:void 0,deps:void 0,depsTail:void 0,flags:+!r,get:()=>(void 0!==t&&f(n,t,b),n._snapshot),subscribe(e){var r;let o,i,s=g(e),a={current:!1},l=(r=()=>{n.get(),a.current?s.next?.(n._snapshot):a.current=!0},o=()=>{let e=t;t=i,++b,i.depsTail=void 0,i.flags=6;try{return r()}finally{t=e,i.flags&=-5,E(i)}},i={deps:void 0,depsTail:void 0,subs:void 0,subsTail:void 0,flags:6,notify(){let e=this.flags;16&e||32&e&&k(this.deps,this)?o():this.flags=2},stop(){this.flags=0,this.depsTail=void 0,E(this)}},o(),i);return{unsubscribe:()=>{l.stop()}}},_update(o){let i=t,s=(void 0)??Object.is;if(r)t=n,++b,n.depsTail=void 0;else if(void 0===o)return!1;r&&(n.flags=5);try{let t=n._snapshot,i="function"==typeof o?o(t):void 0===o&&r?e(t):o;if(void 0===t||!s(t,i))return n._snapshot=i,!0;return!1}finally{t=i,r&&(n.flags&=-5),E(n)}}};return r?(n.flags=17,n.get=function(){let e=n.flags;if(16&e||32&e&&k(n.deps,n)){if(n._update()){let e=n.subs;void 0!==e&&_(e)}}else 32&e&&(n.flags=-33&e);return void 0!==t&&f(n,t,b),n._snapshot}):n.set=function(e){if(n._update(e)){let e=n.subs;if(void 0!==e&&(x(e),_(e),1)){for(;y<w;){let e=m[y];m[y++]=void 0,e.notify()}y=0,w=0}}},n}(e),this.get=this.get.bind(this),this.setState=this.setState.bind(this),this.subscribe=this.subscribe.bind(this),r&&(this.actions=r(this))}setState(e){this.atom.set(e)}get state(){return this.atom.get()}get(){return this.state}subscribe(e){return this.atom.subscribe(g(e))}};function T(){return{canLeadingExecute:!0,executionCount:0,isPending:!1,lastArgs:void 0,status:"idle",maybeExecuteCount:0}}let j={enabled:!0,leading:!1,trailing:!0,wait:0};var S=class{#b;constructor(e,t){this.fn=e,this.store=new C(T()),this.setOptions=e=>{this.options={...this.options,...e},this.#f()||this.cancel()},this.#v=e=>{this.store.setState(t=>{let r={...t,...e},{isPending:n}=r;return{...r,status:this.#f()?n?"pending":"idle":"disabled"}}),((e,t)=>{let r=t.key;if(r){var n,o;d.set(r,t),h.emit(e,{key:(n={...t,key:r}).key,store:{state:p("function"==typeof(o=n.store).get?o.get():o.state)},options:p(n.options)})}})("Debouncer",this)},this.#f=()=>!!u(this.options.enabled,this),this.#x=()=>u(this.options.wait,this),this.maybeExecute=(...e)=>{if(!this.#f())return;this.#v({maybeExecuteCount:this.store.state.maybeExecuteCount+1});let t=!1;this.options.leading&&this.store.state.canLeadingExecute&&(this.#v({canLeadingExecute:!1}),t=!0,this.#k(...e)),this.options.trailing&&this.#v({isPending:!0,lastArgs:e}),this.#b&&clearTimeout(this.#b),this.#b=setTimeout(()=>{this.#v({canLeadingExecute:!0}),this.options.trailing&&!t&&this.#k(...e)},this.#x())},this.#k=(...e)=>{this.#f()&&(this.fn(...e),this.#v({executionCount:this.store.state.executionCount+1,isPending:!1,lastArgs:void 0}),this.options.onExecute?.(e,this))},this.flush=()=>{this.store.state.isPending&&this.store.state.lastArgs&&(this.#_(),this.#k(...this.store.state.lastArgs))},this.#_=()=>{this.#b&&(clearTimeout(this.#b),this.#b=void 0)},this.cancel=()=>{this.#_(),this.#v({canLeadingExecute:!0,isPending:!1})},this.reset=()=>{this.#v(T())},this.key=t.key,this.options={...j,...t},this.#v(this.options.initialState??{}),this.key&&h.on("d-Debouncer",e=>{e.payload.key===this.key&&(this.#v(e.payload.store.state),this.setOptions(e.payload.options))})}#v;#f;#x;#k;#_};e.s(["useDebouncer",0,function(e,t,i=()=>({})){let s={...((0,r.useContext)(n)?.defaultOptions??{}).debouncer,...t},[a]=(0,r.useState)(()=>{let t=new S(e,s);return t.Subscribe=function(e){let r=l(t.store,e.selector,{compare:o});return"function"==typeof e.children?e.children(r):e.children},t});a.fn=e,a.setOptions(s),(0,r.useEffect)(()=>()=>{s.onUnmount?s.onUnmount(a):a.cancel()},[]);let u=l(a.store,i,{compare:o});return(0,r.useMemo)(()=>({...a,state:u}),[a,u])}],540626)},586448,e=>{"use strict";var t=e.i(271645),r=e.i(540143),n=e.i(869230),o=e.i(915823),i=e.i(619273);function s(e,t){let r=new Set(t);return e.filter(e=>!r.has(e))}var a=class extends o.Subscribable{#y;#w;#E;#C;#T;#j;#S;#N;#O;#I=[];constructor(e,t,r){super(),this.#y=e,this.#C=r,this.#E=[],this.#T=[],this.#w=[],this.setQueries(t)}onSubscribe(){1===this.listeners.size&&this.#T.forEach(e=>{e.subscribe(t=>{this.#A(e,t)})})}onUnsubscribe(){this.listeners.size||this.destroy()}destroy(){this.listeners=new Set,this.#T.forEach(e=>{e.destroy()})}setQueries(e,t){this.#E=e,this.#C=t,r.notifyManager.batch(()=>{let e=this.#T,t=this.#L(this.#E);t.forEach(e=>e.observer.setOptions(e.defaultedQueryOptions));let r=t.map(e=>e.observer),n=r.map(e=>e.getCurrentResult()),o=e.length!==r.length,a=r.some((t,r)=>t!==e[r]),l=o||a,u=!!l||n.some((e,t)=>{let r=this.#w[t];return!r||!(0,i.shallowEqualObjects)(e,r)});(l||u)&&(l&&(this.#I=t,this.#T=r),this.#w=n,this.hasListeners()&&(l&&(s(e,r).forEach(e=>{e.destroy()}),s(r,e).forEach(e=>{e.subscribe(t=>{this.#A(e,t)})})),this.#R()))})}getCurrentResult(){return this.#w}getQueries(){return this.#T.map(e=>e.getCurrentQuery())}getObservers(){return this.#T}getOptimisticResult(e,t){let r=this.#L(e),n=r.map(e=>e.observer.getOptimisticResult(e.defaultedQueryOptions)),o=r.map(e=>e.defaultedQueryOptions.queryHash);return[n,e=>this.#$(e??n,t,o),()=>this.#M(n,r)]}#M(e,t){return t.map((r,n)=>{let o=e[n];return r.defaultedQueryOptions.notifyOnChangeProps?o:r.observer.trackResult(o,e=>{t.forEach(t=>{t.observer.trackProp(e)})})})}#$(e,t,r){if(t){let n=this.#O,o=void 0!==r&&void 0!==n&&(n.length!==r.length||r.some((e,t)=>e!==n[t]));return(!this.#j||this.#w!==this.#N||o||t!==this.#S)&&(this.#S=t,this.#N=this.#w,void 0!==r&&(this.#O=r),this.#j=(0,i.replaceEqualDeep)(this.#j,t(e))),this.#j}return e}#H(){return this.#C?.combine!==void 0&&this.#T.some((e,t)=>e.options.suspense&&this.#w[t]?.data===void 0)}#L(e){let t=new Map;this.#T.forEach(e=>{let r=e.options.queryHash;if(!r)return;let n=t.get(r);n?n.push(e):t.set(r,[e])});let r=[];return e.forEach(e=>{let o=this.#y.defaultQueryOptions(e),i=t.get(o.queryHash)?.shift()??new n.QueryObserver(this.#y,o);r.push({defaultedQueryOptions:o,observer:i})}),r}#A(e,t){let r=this.#T.indexOf(e);if(-1!==r){var n;let e;this.#w=(n=this.#w,(e=n.slice(0))[r]=t,e),this.#R()}}#R(){if(this.hasListeners()){let e=this.#M(this.#w,this.#I),t=this.#H(),n=this.#j,o=t?n:this.#$(e,this.#C?.combine);(t||n!==o)&&r.notifyManager.batch(()=>{this.listeners.forEach(e=>{e(this.#w)})})}}},l=e.i(912598),u=e.i(381384),c=e.i(673664),d=e.i(427001),p=e.i(254440);e.s(["useQueries",0,function({queries:e,...o},s){let h=(0,l.useQueryClient)(s),g=(0,u.useIsRestoring)(),m=(0,c.useQueryErrorResetBoundary)(),b=t.useMemo(()=>e.map(e=>{let t=h.defaultQueryOptions(e);return t._optimisticResults=g?"isRestoring":"optimistic",t}),[e,h,g]);b.forEach(e=>{(0,p.ensureSuspenseTimers)(e);let t=h.getQueryCache().get(e.queryHash);(0,d.ensurePreventErrorBoundaryRetry)(e,m,t)}),(0,d.useClearResetErrorBoundary)(m);let[f]=t.useState(()=>new a(h,b,o)),[v,x,k]=f.getOptimisticResult(b,o.combine),_=!g&&!1!==o.subscribed;t.useSyncExternalStore(t.useCallback(e=>_?f.subscribe(r.notifyManager.batchCalls(e)):i.noop,[f,_]),()=>f.getCurrentResult(),()=>f.getCurrentResult()),t.useEffect(()=>{f.setQueries(b,o)},[b,o,f]);let y=v.some((e,t)=>(0,p.shouldSuspend)(b[t],e))?v.flatMap((e,t)=>{let r=b[t];if(r&&(0,p.shouldSuspend)(r,e)){let e=new n.QueryObserver(h,r);return(0,p.fetchOptimistic)(r,e,m)}return[]}):[];if(y.length>0)throw Promise.all(y);let w=v.find((e,t)=>{let r=b[t];return r&&(0,d.getHasError)({result:e,errorResetBoundary:m,throwOnError:r.throwOnError,query:h.getQueryCache().get(r.queryHash),suspense:r.suspense})});if(w?.error)throw w.error;return x(k())}],586448)},546467,e=>{"use strict";let t=(0,e.i(475254).default)("external-link",[["path",{d:"M15 3h6v6",key:"1q9fwt"}],["path",{d:"M10 14 21 3",key:"gplh6r"}],["path",{d:"M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6",key:"a6xqqp"}]]);e.s(["default",0,t])},778917,e=>{"use strict";var t=e.i(546467);e.s(["ExternalLink",()=>t.default])},306228,e=>{"use strict";let t=(0,e.i(475254).default)("link-2",[["path",{d:"M9 17H7A5 5 0 0 1 7 7h2",key:"8i5ue5"}],["path",{d:"M15 7h2a5 5 0 1 1 0 10h-2",key:"1b9ql8"}],["line",{x1:"8",x2:"16",y1:"12",y2:"12",key:"1jonct"}]]);e.s(["Link2",0,t],306228)},531278,e=>{"use strict";var t=e.i(717521);e.s(["Loader2",()=>t.default])},455037,e=>{"use strict";var t=e.i(494144);e.s(["prism",()=>t.default])},198458,e=>{"use strict";var t=e.i(655063),r=e.i(266027),n=e.i(271645),o=e.i(741466);e.s(["useResourceList",0,function(e){let{queryKey:i,fetchPage:s,serializeFilters:a,defaultSorting:l,defaultPageSize:u,enabled:c}=e,[d,p]=(0,n.useState)(l),[h,g]=(0,n.useState)({pageIndex:0,pageSize:u}),[m,b]=(0,n.useState)([]),[f,v]=(0,n.useState)(""),[x]=(0,t.useDebouncedValue)(f,{wait:o.DEBOUNCE_WAIT_MS}),k=(0,n.useMemo)(()=>{let e=d.map(e=>e.desc?`-${e.id}`:e.id).join(","),t=x.trim();return{page:h.pageIndex+1,page_size:h.pageSize,...""===e?{}:{sort:e},...""===t?{}:{q:t},...a(m)}},[d,h.pageIndex,h.pageSize,x,m,a]),_={queryKey:[...i,k],queryFn:({signal:e})=>s(k,e),enabled:c,placeholderData:e=>e},{data:y,isLoading:w,isPlaceholderData:E,isFetching:C,error:T,refetch:j}=(0,r.useQuery)(_),S=(0,n.useCallback)(()=>g(e=>({...e,pageIndex:0})),[]),N=(0,n.useCallback)(e=>{p(e),S()},[S]),O=(0,n.useCallback)(e=>{b(e),S()},[S]),I=(0,n.useCallback)(e=>{v(e),S()},[S]),A=(0,n.useCallback)(()=>{j()},[j]);return{rows:(0,n.useMemo)(()=>y?.data??[],[y]),rowCount:y?.meta.total_count??0,isLoading:w||E,isFetching:C,error:T,refetch:A,sorting:d,onSortingChange:N,pagination:h,onPaginationChange:g,columnFilters:m,onColumnFiltersChange:O,searchValue:f,onSearchChange:I}}])},466828,e=>{"use strict";var t=e.i(843476),r=e.i(271645),n=e.i(678784);let o=(0,e.i(475254).default)("clipboard",[["rect",{width:"8",height:"4",x:"8",y:"2",rx:"1",ry:"1",key:"tgr4d6"}],["path",{d:"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2",key:"116196"}]]);var i=e.i(650056);let s={'code[class*="language-"]':{background:"hsl(230, 1%, 98%)",color:"hsl(230, 8%, 24%)",fontFamily:'"Fira Code", "Fira Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace',direction:"ltr",textAlign:"left",whiteSpace:"pre",wordSpacing:"normal",wordBreak:"normal",lineHeight:"1.5",MozTabSize:"2",OTabSize:"2",tabSize:"2",WebkitHyphens:"none",MozHyphens:"none",msHyphens:"none",hyphens:"none"},'pre[class*="language-"]':{background:"hsl(230, 1%, 98%)",color:"hsl(230, 8%, 24%)",fontFamily:'"Fira Code", "Fira Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace',direction:"ltr",textAlign:"left",whiteSpace:"pre",wordSpacing:"normal",wordBreak:"normal",lineHeight:"1.5",MozTabSize:"2",OTabSize:"2",tabSize:"2",WebkitHyphens:"none",MozHyphens:"none",msHyphens:"none",hyphens:"none",padding:"1em",margin:"0.5em 0",overflow:"auto",borderRadius:"0.3em"},'code[class*="language-"]::-moz-selection':{background:"hsl(230, 1%, 90%)",color:"inherit"},'code[class*="language-"] *::-moz-selection':{background:"hsl(230, 1%, 90%)",color:"inherit"},'pre[class*="language-"] *::-moz-selection':{background:"hsl(230, 1%, 90%)",color:"inherit"},'code[class*="language-"]::selection':{background:"hsl(230, 1%, 90%)",color:"inherit"},'code[class*="language-"] *::selection':{background:"hsl(230, 1%, 90%)",color:"inherit"},'pre[class*="language-"] *::selection':{background:"hsl(230, 1%, 90%)",color:"inherit"},':not(pre) > code[class*="language-"]':{padding:"0.2em 0.3em",borderRadius:"0.3em",whiteSpace:"normal"},comment:{color:"hsl(230, 4%, 64%)",fontStyle:"italic"},prolog:{color:"hsl(230, 4%, 64%)"},cdata:{color:"hsl(230, 4%, 64%)"},doctype:{color:"hsl(230, 8%, 24%)"},punctuation:{color:"hsl(230, 8%, 24%)"},entity:{color:"hsl(230, 8%, 24%)",cursor:"help"},"attr-name":{color:"hsl(35, 99%, 36%)"},"class-name":{color:"hsl(35, 99%, 36%)"},boolean:{color:"hsl(35, 99%, 36%)"},constant:{color:"hsl(35, 99%, 36%)"},number:{color:"hsl(35, 99%, 36%)"},atrule:{color:"hsl(35, 99%, 36%)"},keyword:{color:"hsl(301, 63%, 40%)"},property:{color:"hsl(5, 74%, 59%)"},tag:{color:"hsl(5, 74%, 59%)"},symbol:{color:"hsl(5, 74%, 59%)"},deleted:{color:"hsl(5, 74%, 59%)"},important:{color:"hsl(5, 74%, 59%)"},selector:{color:"hsl(119, 34%, 47%)"},string:{color:"hsl(119, 34%, 47%)"},char:{color:"hsl(119, 34%, 47%)"},builtin:{color:"hsl(119, 34%, 47%)"},inserted:{color:"hsl(119, 34%, 47%)"},regex:{color:"hsl(119, 34%, 47%)"},"attr-value":{color:"hsl(119, 34%, 47%)"},"attr-value > .token.punctuation":{color:"hsl(119, 34%, 47%)"},variable:{color:"hsl(221, 87%, 60%)"},operator:{color:"hsl(221, 87%, 60%)"},function:{color:"hsl(221, 87%, 60%)"},url:{color:"hsl(198, 99%, 37%)"},"attr-value > .token.punctuation.attr-equals":{color:"hsl(230, 8%, 24%)"},"special-attr > .token.attr-value > .token.value.css":{color:"hsl(230, 8%, 24%)"},".language-css .token.selector":{color:"hsl(5, 74%, 59%)"},".language-css .token.property":{color:"hsl(230, 8%, 24%)"},".language-css .token.function":{color:"hsl(198, 99%, 37%)"},".language-css .token.url > .token.function":{color:"hsl(198, 99%, 37%)"},".language-css .token.url > .token.string.url":{color:"hsl(119, 34%, 47%)"},".language-css .token.important":{color:"hsl(301, 63%, 40%)"},".language-css .token.atrule .token.rule":{color:"hsl(301, 63%, 40%)"},".language-javascript .token.operator":{color:"hsl(301, 63%, 40%)"},".language-javascript .token.template-string > .token.interpolation > .token.interpolation-punctuation.punctuation":{color:"hsl(344, 84%, 43%)"},".language-json .token.operator":{color:"hsl(230, 8%, 24%)"},".language-json .token.null.keyword":{color:"hsl(35, 99%, 36%)"},".language-markdown .token.url":{color:"hsl(230, 8%, 24%)"},".language-markdown .token.url > .token.operator":{color:"hsl(230, 8%, 24%)"},".language-markdown .token.url-reference.url > .token.string":{color:"hsl(230, 8%, 24%)"},".language-markdown .token.url > .token.content":{color:"hsl(221, 87%, 60%)"},".language-markdown .token.url > .token.url":{color:"hsl(198, 99%, 37%)"},".language-markdown .token.url-reference.url":{color:"hsl(198, 99%, 37%)"},".language-markdown .token.blockquote.punctuation":{color:"hsl(230, 4%, 64%)",fontStyle:"italic"},".language-markdown .token.hr.punctuation":{color:"hsl(230, 4%, 64%)",fontStyle:"italic"},".language-markdown .token.code-snippet":{color:"hsl(119, 34%, 47%)"},".language-markdown .token.bold .token.content":{color:"hsl(35, 99%, 36%)"},".language-markdown .token.italic .token.content":{color:"hsl(301, 63%, 40%)"},".language-markdown .token.strike .token.content":{color:"hsl(5, 74%, 59%)"},".language-markdown .token.strike .token.punctuation":{color:"hsl(5, 74%, 59%)"},".language-markdown .token.list.punctuation":{color:"hsl(5, 74%, 59%)"},".language-markdown .token.title.important > .token.punctuation":{color:"hsl(5, 74%, 59%)"},bold:{fontWeight:"bold"},italic:{fontStyle:"italic"},namespace:{Opacity:"0.8"},"token.tab:not(:empty):before":{color:"hsla(230, 8%, 24%, 0.2)"},"token.cr:before":{color:"hsla(230, 8%, 24%, 0.2)"},"token.lf:before":{color:"hsla(230, 8%, 24%, 0.2)"},"token.space:before":{color:"hsla(230, 8%, 24%, 0.2)"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item":{marginRight:"0.4em"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > button":{background:"hsl(230, 1%, 90%)",color:"hsl(230, 6%, 44%)",padding:"0.1em 0.4em",borderRadius:"0.3em"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > a":{background:"hsl(230, 1%, 90%)",color:"hsl(230, 6%, 44%)",padding:"0.1em 0.4em",borderRadius:"0.3em"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > span":{background:"hsl(230, 1%, 90%)",color:"hsl(230, 6%, 44%)",padding:"0.1em 0.4em",borderRadius:"0.3em"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > button:hover":{background:"hsl(230, 1%, 78%)",color:"hsl(230, 8%, 24%)"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > button:focus":{background:"hsl(230, 1%, 78%)",color:"hsl(230, 8%, 24%)"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > a:hover":{background:"hsl(230, 1%, 78%)",color:"hsl(230, 8%, 24%)"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > a:focus":{background:"hsl(230, 1%, 78%)",color:"hsl(230, 8%, 24%)"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > span:hover":{background:"hsl(230, 1%, 78%)",color:"hsl(230, 8%, 24%)"},"div.code-toolbar > .toolbar.toolbar > .toolbar-item > span:focus":{background:"hsl(230, 1%, 78%)",color:"hsl(230, 8%, 24%)"},".line-highlight.line-highlight":{background:"hsla(230, 8%, 24%, 0.05)"},".line-highlight.line-highlight:before":{background:"hsl(230, 1%, 90%)",color:"hsl(230, 8%, 24%)",padding:"0.1em 0.6em",borderRadius:"0.3em",boxShadow:"0 2px 0 0 rgba(0, 0, 0, 0.2)"},".line-highlight.line-highlight[data-end]:after":{background:"hsl(230, 1%, 90%)",color:"hsl(230, 8%, 24%)",padding:"0.1em 0.6em",borderRadius:"0.3em",boxShadow:"0 2px 0 0 rgba(0, 0, 0, 0.2)"},"pre[id].linkable-line-numbers.linkable-line-numbers span.line-numbers-rows > span:hover:before":{backgroundColor:"hsla(230, 8%, 24%, 0.05)"},".line-numbers.line-numbers .line-numbers-rows":{borderRightColor:"hsla(230, 8%, 24%, 0.2)"},".command-line .command-line-prompt":{borderRightColor:"hsla(230, 8%, 24%, 0.2)"},".line-numbers .line-numbers-rows > span:before":{color:"hsl(230, 1%, 62%)"},".command-line .command-line-prompt > span:before":{color:"hsl(230, 1%, 62%)"},".rainbow-braces .token.token.punctuation.brace-level-1":{color:"hsl(5, 74%, 59%)"},".rainbow-braces .token.token.punctuation.brace-level-5":{color:"hsl(5, 74%, 59%)"},".rainbow-braces .token.token.punctuation.brace-level-9":{color:"hsl(5, 74%, 59%)"},".rainbow-braces .token.token.punctuation.brace-level-2":{color:"hsl(119, 34%, 47%)"},".rainbow-braces .token.token.punctuation.brace-level-6":{color:"hsl(119, 34%, 47%)"},".rainbow-braces .token.token.punctuation.brace-level-10":{color:"hsl(119, 34%, 47%)"},".rainbow-braces .token.token.punctuation.brace-level-3":{color:"hsl(221, 87%, 60%)"},".rainbow-braces .token.token.punctuation.brace-level-7":{color:"hsl(221, 87%, 60%)"},".rainbow-braces .token.token.punctuation.brace-level-11":{color:"hsl(221, 87%, 60%)"},".rainbow-braces .token.token.punctuation.brace-level-4":{color:"hsl(301, 63%, 40%)"},".rainbow-braces .token.token.punctuation.brace-level-8":{color:"hsl(301, 63%, 40%)"},".rainbow-braces .token.token.punctuation.brace-level-12":{color:"hsl(301, 63%, 40%)"},"pre.diff-highlight > code .token.token.deleted:not(.prefix)":{backgroundColor:"hsla(353, 100%, 66%, 0.15)"},"pre > code.diff-highlight .token.token.deleted:not(.prefix)":{backgroundColor:"hsla(353, 100%, 66%, 0.15)"},"pre.diff-highlight > code .token.token.deleted:not(.prefix)::-moz-selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre.diff-highlight > code .token.token.deleted:not(.prefix) *::-moz-selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre > code.diff-highlight .token.token.deleted:not(.prefix)::-moz-selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre > code.diff-highlight .token.token.deleted:not(.prefix) *::-moz-selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre.diff-highlight > code .token.token.deleted:not(.prefix)::selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre.diff-highlight > code .token.token.deleted:not(.prefix) *::selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre > code.diff-highlight .token.token.deleted:not(.prefix)::selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre > code.diff-highlight .token.token.deleted:not(.prefix) *::selection":{backgroundColor:"hsla(353, 95%, 66%, 0.25)"},"pre.diff-highlight > code .token.token.inserted:not(.prefix)":{backgroundColor:"hsla(137, 100%, 55%, 0.15)"},"pre > code.diff-highlight .token.token.inserted:not(.prefix)":{backgroundColor:"hsla(137, 100%, 55%, 0.15)"},"pre.diff-highlight > code .token.token.inserted:not(.prefix)::-moz-selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},"pre.diff-highlight > code .token.token.inserted:not(.prefix) *::-moz-selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},"pre > code.diff-highlight .token.token.inserted:not(.prefix)::-moz-selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},"pre > code.diff-highlight .token.token.inserted:not(.prefix) *::-moz-selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},"pre.diff-highlight > code .token.token.inserted:not(.prefix)::selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},"pre.diff-highlight > code .token.token.inserted:not(.prefix) *::selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},"pre > code.diff-highlight .token.token.inserted:not(.prefix)::selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},"pre > code.diff-highlight .token.token.inserted:not(.prefix) *::selection":{backgroundColor:"hsla(135, 73%, 55%, 0.25)"},".prism-previewer.prism-previewer:before":{borderColor:"hsl(0, 0, 95%)"},".prism-previewer-gradient.prism-previewer-gradient div":{borderColor:"hsl(0, 0, 95%)",borderRadius:"0.3em"},".prism-previewer-color.prism-previewer-color:before":{borderRadius:"0.3em"},".prism-previewer-easing.prism-previewer-easing:before":{borderRadius:"0.3em"},".prism-previewer.prism-previewer:after":{borderTopColor:"hsl(0, 0, 95%)"},".prism-previewer-flipped.prism-previewer-flipped.after":{borderBottomColor:"hsl(0, 0, 95%)"},".prism-previewer-angle.prism-previewer-angle:before":{background:"hsl(0, 0%, 100%)"},".prism-previewer-time.prism-previewer-time:before":{background:"hsl(0, 0%, 100%)"},".prism-previewer-easing.prism-previewer-easing":{background:"hsl(0, 0%, 100%)"},".prism-previewer-angle.prism-previewer-angle circle":{stroke:"hsl(230, 8%, 24%)",strokeOpacity:"1"},".prism-previewer-time.prism-previewer-time circle":{stroke:"hsl(230, 8%, 24%)",strokeOpacity:"1"},".prism-previewer-easing.prism-previewer-easing circle":{stroke:"hsl(230, 8%, 24%)",fill:"transparent"},".prism-previewer-easing.prism-previewer-easing path":{stroke:"hsl(230, 8%, 24%)"},".prism-previewer-easing.prism-previewer-easing line":{stroke:"hsl(230, 8%, 24%)"}};var a=e.i(488012);e.s(["default",0,({code:e,language:l})=>{let u=(0,a.useSyntaxTheme)(s),[c,d]=(0,r.useState)(!1);return(0,t.jsxs)("div",{className:"relative rounded-lg border border-border bg-muted overflow-hidden",children:[(0,t.jsx)("button",{onClick:()=>{navigator.clipboard.writeText(e),d(!0),setTimeout(()=>d(!1),2e3)},className:"absolute top-3 right-3 p-2 rounded-md border border-border bg-background text-muted-foreground hover:bg-accent hover:text-foreground z-raised","aria-label":"Copy code",children:c?(0,t.jsx)(n.CheckIcon,{size:16}):(0,t.jsx)(o,{size:16})}),(0,t.jsx)(i.Prism,{language:l,style:u,customStyle:{margin:0,padding:"1.5rem",borderRadius:"0.5rem",fontSize:"0.9rem",background:"transparent"},codeTagProps:{style:{background:"transparent"}},showLineNumbers:!0,children:e})]})}],466828)},909947,e=>{"use strict";var t=e.i(865361);e.s(["generateCodeSnippet",0,e=>{let r,{apiKeySource:n,accessToken:o,apiKey:i,inputMessage:s,chatHistory:a,selectedTags:l,selectedVectorStores:u,selectedGuardrails:c,selectedPolicies:d,selectedVoice:p,endpointType:h,selectedModel:g,selectedSdk:m,proxySettings:b,customHeaders:f}=e,v="session"===n?o:i,x=window.location.origin,k=b?.WAYPOINT_UI_API_DOC_BASE_URL;k&&k.trim()?x=k:b?.PROXY_BASE_URL&&(x=b.PROXY_BASE_URL);let _=s||"Your prompt here",y=_.replace(/\\/g,"\\\\").replace(/"/g,'\\"').replace(/\n/g,"\\n"),w=a.filter(e=>!e.isImage).map(({role:e,content:t})=>({role:e,content:t})),E={};l.length>0&&(E.tags=l),u.length>0&&(E.vector_stores=u),c.length>0&&(E.guardrails=c),d.length>0&&(E.policies=d);let C=g||"your-model-name",T=f&&Object.keys(f).length>0?`,
	default_headers=${JSON.stringify(f,null,2).replace(/\n/g,"\n	")}`:"",j="azure"===m?`import openai

client = openai.AzureOpenAI(
	api_key="${v||"YOUR_LITELLM_API_KEY"}",
	azure_endpoint="${x}",
	api_version="2024-02-01"${T}
)`:`import openai

client = openai.OpenAI(
	api_key="${v||"YOUR_LITELLM_API_KEY"}",
	base_url="${x}"${T}
)`;switch(h){case t.EndpointType.CHAT:{let e=Object.keys(E).length>0,t="";if(e){let e=JSON.stringify({metadata:E},null,2).split("\n").map(e=>" ".repeat(4)+e).join("\n").trim();t=`,
    extra_body=${e}`}let n=w.length>0?w:[{role:"user",content:_}];r=`
import base64

# Helper function to encode images to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Example with text only
response = client.chat.completions.create(
    model="${C}",
    messages=${JSON.stringify(n,null,4)}${t}
)

print(response)

# Example with image or PDF (uncomment and provide file path to use)
# base64_file = encode_image("path/to/your/file.jpg")  # or .pdf
# response_with_file = client.chat.completions.create(
#     model="${C}",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "${y}"
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_file}"  # or data:application/pdf;base64,{base64_file}
#                     }
#                 }
#             ]
#         }
#     ]${t}
# )
# print(response_with_file)
`;break}case t.EndpointType.RESPONSES:{let e=Object.keys(E).length>0,t="";if(e){let e=JSON.stringify({metadata:E},null,2).split("\n").map(e=>" ".repeat(4)+e).join("\n").trim();t=`,
    extra_body=${e}`}let n=w.length>0?w:[{role:"user",content:_}];r=`
import base64

# Helper function to encode images to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Example with text only
response = client.responses.create(
    model="${C}",
    input=${JSON.stringify(n,null,4)}${t}
)

print(response.output_text)

# Example with image or PDF (uncomment and provide file path to use)
# base64_file = encode_image("path/to/your/file.jpg")  # or .pdf
# response_with_file = client.responses.create(
#     model="${C}",
#     input=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "input_text", "text": "${y}"},
#                 {
#                     "type": "input_image",
#                     "image_url": f"data:image/jpeg;base64,{base64_file}",  # or data:application/pdf;base64,{base64_file}
#                 },
#             ],
#         }
#     ]${t}
# )
# print(response_with_file.output_text)
`;break}case t.EndpointType.IMAGE:r="azure"===m?`
# NOTE: The Azure SDK does not have a direct equivalent to the multi-modal 'responses.create' method shown for OpenAI.
# This snippet uses 'client.images.generate' and will create a new image based on your prompt.
# It does not use the uploaded image, as 'client.images.generate' does not support image inputs in this context.
import os
import requests
import json
import time
from PIL import Image

result = client.images.generate(
	model="${C}",
	prompt="${s}",
	n=1
)

json_response = json.loads(result.model_dump_json())

# Set the directory for the stored image
image_dir = os.path.join(os.curdir, 'images')

# If the directory doesn't exist, create it
if not os.path.isdir(image_dir):
	os.mkdir(image_dir)

# Initialize the image path
image_filename = f"generated_image_{int(time.time())}.png"
image_path = os.path.join(image_dir, image_filename)

try:
	# Retrieve the generated image
	if json_response.get("data") && len(json_response["data"]) > 0 && json_response["data"][0].get("url"):
			image_url = json_response["data"][0]["url"]
			generated_image = requests.get(image_url).content
			with open(image_path, "wb") as image_file:
					image_file.write(generated_image)

			print(f"Image saved to {image_path}")
			# Display the image
			image = Image.open(image_path)
			image.show()
	else:
			print("Could not find image URL in response.")
			print("Full response:", json_response)
except Exception as e:
	print(f"An error occurred: {e}")
	print("Full response:", json_response)
`:`
import base64
import os
import time
import json
from PIL import Image
import requests

# Helper function to encode images to base64
def encode_image(image_path):
	with open(image_path, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode('utf-8')

# Helper function to create a file (simplified for this example)
def create_file(image_path):
	# In a real implementation, this would upload the file to OpenAI
	# For this example, we'll just return a placeholder ID
	return f"file_{os.path.basename(image_path).replace('.', '_')}"

# The prompt entered by the user
prompt = "${y}"

# Encode images to base64
base64_image1 = encode_image("body-lotion.png")
base64_image2 = encode_image("soap.png")

# Create file IDs
file_id1 = create_file("body-lotion.png")
file_id2 = create_file("incense-kit.png")

response = client.responses.create(
	model="${C}",
	input=[
			{
					"role": "user",
					"content": [
							{"type": "input_text", "text": prompt},
							{
									"type": "input_image",
									"image_url": f"data:image/jpeg;base64,{base64_image1}",
							},
							{
									"type": "input_image",
									"image_url": f"data:image/jpeg;base64,{base64_image2}",
							},
							{
									"type": "input_image",
									"file_id": file_id1,
							},
							{
									"type": "input_image",
									"file_id": file_id2,
							}
					],
			}
	],
	tools=[{"type": "image_generation"}],
)

# Process the response
image_generation_calls = [
	output
	for output in response.output
	if output.type == "image_generation_call"
]

image_data = [output.result for output in image_generation_calls]

if image_data:
	image_base64 = image_data[0]
	image_filename = f"edited_image_{int(time.time())}.png"
	with open(image_filename, "wb") as f:
			f.write(base64.b64decode(image_base64))
	print(f"Image saved to {image_filename}")
else:
	# If no image is generated, there might be a text response with an explanation
	text_response = [output.text for output in response.output if hasattr(output, 'text')]
	if text_response:
			print("No image generated. Model response:")
			print("\\n".join(text_response))
	else:
			print("No image data found in response.")
	print("Full response for debugging:")
	print(response)
`;break;case t.EndpointType.IMAGE_EDITS:r="azure"===m?`
import base64
import os
import time
import json
from PIL import Image
import requests

# Helper function to encode images to base64
def encode_image(image_path):
	with open(image_path, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode('utf-8')

# The prompt entered by the user
prompt = "${y}"

# Encode images to base64
base64_image1 = encode_image("body-lotion.png")
base64_image2 = encode_image("soap.png")

# Create file IDs
file_id1 = create_file("body-lotion.png")
file_id2 = create_file("incense-kit.png")

response = client.responses.create(
	model="${C}",
	input=[
			{
					"role": "user",
					"content": [
							{"type": "input_text", "text": prompt},
							{
									"type": "input_image",
									"image_url": f"data:image/jpeg;base64,{base64_image1}",
							},
							{
									"type": "input_image",
									"image_url": f"data:image/jpeg;base64,{base64_image2}",
							},
							{
									"type": "input_image",
									"file_id": file_id1,
							},
							{
									"type": "input_image",
									"file_id": file_id2,
							}
					],
			}
	],
	tools=[{"type": "image_generation"}],
)

# Process the response
image_generation_calls = [
	output
	for output in response.output
	if output.type == "image_generation_call"
]

image_data = [output.result for output in image_generation_calls]

if image_data:
	image_base64 = image_data[0]
	image_filename = f"edited_image_{int(time.time())}.png"
	with open(image_filename, "wb") as f:
			f.write(base64.b64decode(image_base64))
	print(f"Image saved to {image_filename}")
else:
	# If no image is generated, there might be a text response with an explanation
	text_response = [output.text for output in response.output if hasattr(output, 'text')]
	if text_response:
			print("No image generated. Model response:")
			print("\\n".join(text_response))
	else:
			print("No image data found in response.")
	print("Full response for debugging:")
	print(response)
`:`
import base64
import os
import time

# Helper function to encode images to base64
def encode_image(image_path):
	with open(image_path, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode('utf-8')

# Helper function to create a file (simplified for this example)
def create_file(image_path):
	# In a real implementation, this would upload the file to OpenAI
	# For this example, we'll just return a placeholder ID
	return f"file_{os.path.basename(image_path).replace('.', '_')}"

# The prompt entered by the user
prompt = "${y}"

# Encode images to base64
base64_image1 = encode_image("body-lotion.png")
base64_image2 = encode_image("soap.png")

# Create file IDs
file_id1 = create_file("body-lotion.png")
file_id2 = create_file("incense-kit.png")

response = client.responses.create(
	model="${C}",
	input=[
			{
					"role": "user",
					"content": [
							{"type": "input_text", "text": prompt},
							{
									"type": "input_image",
									"image_url": f"data:image/jpeg;base64,{base64_image1}",
							},
							{
									"type": "input_image",
									"image_url": f"data:image/jpeg;base64,{base64_image2}",
							},
							{
									"type": "input_image",
									"file_id": file_id1,
							},
							{
									"type": "input_image",
									"file_id": file_id2,
							}
					],
			}
	],
	tools=[{"type": "image_generation"}],
)

# Process the response
image_generation_calls = [
	output
	for output in response.output
	if output.type == "image_generation_call"
]

image_data = [output.result for output in image_generation_calls]

if image_data:
	image_base64 = image_data[0]
	image_filename = f"edited_image_{int(time.time())}.png"
	with open(image_filename, "wb") as f:
			f.write(base64.b64decode(image_base64))
	print(f"Image saved to {image_filename}")
else:
	# If no image is generated, there might be a text response with an explanation
	text_response = [output.text for output in response.output if hasattr(output, 'text')]
	if text_response:
			print("No image generated. Model response:")
			print("\\n".join(text_response))
	else:
			print("No image data found in response.")
	print("Full response for debugging:")
	print(response)
`;break;case t.EndpointType.EMBEDDINGS:r=`
response = client.embeddings.create(
	input="${s||"Your string here"}",
	model="${C}",
	encoding_format="base64" # or "float"
)

print(response.data[0].embedding)
`;break;case t.EndpointType.TRANSCRIPTION:r=`
# Open the audio file
audio_file = open("path/to/your/audio/file.mp3", "rb")

# Make the transcription request
response = client.audio.transcriptions.create(
	model="${C}",
	file=audio_file${s?`,
	prompt="${s.replace(/\\/g,"\\\\").replace(/"/g,'\\"')}"`:""}
)

print(response.text)
`;break;case t.EndpointType.SPEECH:r=`
# Make the text-to-speech request
response = client.audio.speech.create(
	model="${C}",
	input="${s||"Your text to convert to speech here"}",
	voice="${p}"  # Options: alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer
)

# Save the audio to a file
output_filename = "output_speech.mp3"
response.stream_to_file(output_filename)
print(f"Audio saved to {output_filename}")

# Optional: Customize response format and speed
# response = client.audio.speech.create(
#     model="${C}",
#     input="${s||"Your text to convert to speech here"}",
#     voice="alloy",
#     response_format="mp3",  # Options: mp3, opus, aac, flac, wav, pcm
#     speed=1.0  # Range: 0.25 to 4.0
# )
# response.stream_to_file("output_speech.mp3")
`;break;default:r="\n# Code generation for this endpoint is not implemented yet."}return`${j}
${r}`}])},652272,209261,e=>{"use strict";var t=e.i(843476),r=e.i(271645),n=e.i(871689),o=e.i(643531),i=e.i(174886),s=e.i(306228),a=e.i(196631);let l=/^[a-zA-Z0-9][a-zA-Z0-9._-]*(\/[a-zA-Z0-9][a-zA-Z0-9._-]*)*$/,u=e=>e.trim().replace(/\/+$/,""),c=/\.(md|markdown|txt|json|ya?ml|toml)$/i,d=/\.zip$/i,p=/^[0-9a-fA-F]{64}$/,h=/^\d{1,3}(\.\d{1,3}){3}$/,g=/^[A-Za-z0-9-]+$/,m=/^[A-Za-z0-9._-]+$/,b=/^https?:\/\//i,f="ssh://",v=/^([a-z0-9._-]+)@([^:/@]+):(?!\/)(.+)$/i,x=e=>e.pathname.split("/").filter(e=>""!==e),k=e=>{try{return new URL(e)}catch{return null}},_=e=>e.hostname.includes(".")&&!e.hostname.startsWith("[")&&!h.test(e.hostname),y=e=>{let t=e.split("/").filter(e=>""!==e);return t[t.length-1]??""},w=e=>e.toLowerCase().replace(/[^a-z0-9-]+/g,"-").replace(/-+/g,"-").replace(/^-+|-+$/g,""),E=(e,t,r,n)=>{let o=u(n??"");return""!==o?l.test(o)?{parsed:{source:"git-subdir",url:t,path:o},label:`${e} subdir — ${t} @ ${o}`,suggestedName:w(y(o))}:null:{parsed:{source:"url",url:t},label:`${e} repo — ${t}`,suggestedName:w(r)}},C=e=>JSON.stringify({extraKnownMarketplaces:{litellm:{source:{source:"url",url:`${e}/claude-code/marketplace.json`}}}},null,2),T=e=>`/plugin install ${e.name}@litellm`,j=e=>"github"===e.source&&e.repo?`GitHub: ${e.repo}`:"git-subdir"===e.source&&e.url&&e.path?`${e.url} @ ${e.path}`:("url"===e.source||"archive"===e.source)&&e.url?e.url:"Unknown source",S=e=>"github"===e.source&&e.repo?`https://github.com/${e.repo}`:("url"===e.source||"git-subdir"===e.source||"archive"===e.source)&&e.url&&b.test(e.url)?e.url:null;e.s(["buildMarketplaceSettingsSnippet",0,C,"formatInstallCommand",0,T,"getCategoryBadgeColor",0,e=>{if(!e)return"gray";let t=e.toLowerCase();if(t.includes("development")||t.includes("dev"))return"blue";if(t.includes("productivity")||t.includes("workflow"))return"green";if(t.includes("learning")||t.includes("education"))return"purple";if(t.includes("security")||t.includes("safety"))return"red";if(t.includes("data")||t.includes("analytics"))return"orange";else if(t.includes("integration")||t.includes("api"))return"yellow";return"gray"},"getSourceDisplayText",0,j,"getSourceLink",0,S,"isValidEmail",0,e=>!e||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e),"isValidSemanticVersion",0,e=>!e||/^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$/.test(e),"isValidSha256",0,e=>""===e.trim()||p.test(e.trim()),"isValidSubPath",0,e=>{let t=u(e);return""!==t&&l.test(t)},"parseKeywords",0,e=>e&&""!==e.trim()?e.split(",").map(e=>e.trim()).filter(e=>""!==e):[],"parseSkillSource",0,(e,t)=>{let r=((e,t)=>{let r=e.trim(),n=v.exec(r),o=n?`${f}${n[1]}@${n[2]}/${n[3]}`:r;if(!o.toLowerCase().startsWith(f))return null;let i=k(o);if(!i||""===i.username||""!==i.password||!_(i))return null;let s=o.indexOf("/",f.length);return -1===s||i.pathname!==o.slice(s)||x(i).length<2?null:E("SSH",r,y(i.pathname).replace(/\.git$/i,""),t)})(e,t);if(r)return r;let n=(e=>{let t=e.trim();if(""===t||t.startsWith("//"))return null;let r=k(/^[a-z][a-z0-9+.-]*:\/\//i.test(t)?t:`https://${t}`);return r&&"https:"===r.protocol&&""===r.username&&""===r.password&&_(r)?r:null})(e);if(!n)return null;if(d.test(n.pathname))return{parsed:{source:"archive",url:n.href},label:`Zip archive — ${n.host}${n.pathname}`,suggestedName:w(y(n.pathname).replace(d,""))};if("github.com"===n.hostname.replace(/^www\./,""))return((e,t)=>{let r=x(e);if(r.length<2)return null;let n=r[0],o=r[1].replace(/\.git$/,"");if(!g.test(n)||!m.test(o))return null;let i=`${n}/${o}`,s=`https://github.com/${i}`,a={parsed:{source:"github",repo:i},label:`GitHub repo — ${i}`,suggestedName:w(o)};if(r.length>=4&&("tree"===r[2]||"blob"===r[2])){let e=r.slice(4),t=y(e.join("/")),n=c.test(t)?e.slice(0,-1):e;if(0===n.length)return a;let o=u(n.join("/"));return l.test(o)?{parsed:{source:"git-subdir",url:s,path:o},label:`GitHub subdir — ${i} @ ${o}`,suggestedName:w(y(o))}:null}if(2!==r.length)return null;let d=u(t??"");return""!==d?l.test(d)?{parsed:{source:"git-subdir",url:s,path:d},label:`GitHub subdir — ${i} @ ${d}`,suggestedName:w(y(d))}:null:a})(n,t);if(x(n).length<2)return null;let o=y(n.pathname).replace(/\.git$/,"");return E("Git",`${n.protocol}//${n.host}${n.pathname.replace(/\/+$/,"")}`,o,t)},"validatePluginName",0,e=>!!e&&""!==e.trim()&&/^[a-z0-9-]+$/.test(e)],209261);let N=({source:e})=>{let r=S(e),n=r&&"git-subdir"===e.source&&e.path?`${r}/tree/main/${e.path}`:r;return n?(0,t.jsxs)("div",{className:"mb-6",children:[(0,t.jsx)("div",{className:"mb-1 text-xs text-muted-foreground",children:"Source"}),(0,t.jsxs)("a",{href:n,target:"_blank",rel:"noopener noreferrer",className:"flex items-center gap-1 break-all text-[13px] text-info",children:[n.replace("https://",""),(0,t.jsx)(s.Link2,{className:"size-3 shrink-0"})]})]}):e.url?(0,t.jsxs)("div",{className:"mb-6",children:[(0,t.jsx)("div",{className:"mb-1 text-xs text-muted-foreground",children:"Source"}),(0,t.jsx)("div",{className:"break-all text-[13px] text-foreground",children:j(e)})]}):null};e.s(["default",0,({skill:e,onBack:s})=>{let[l,u]=(0,r.useState)("overview"),[c,d]=(0,r.useState)(null),p=(e,t)=>{navigator.clipboard.writeText(e),d(t),setTimeout(()=>d(null),2e3)},h=T(e),g=C(window.location.origin),m=[...e.category?[{property:"Category",value:e.category}]:[],...e.domain?[{property:"Domain",value:e.domain}]:[],...e.namespace?[{property:"Namespace",value:e.namespace}]:[],...e.version?[{property:"Version",value:e.version}]:[],...e.author?.name?[{property:"Author",value:e.author.name}]:[],...e.created_at?[{property:"Added",value:new Date(e.created_at).toLocaleDateString()}]:[]];return(0,t.jsxs)("div",{className:"py-6 pl-0 pr-8",children:[(0,t.jsxs)("div",{onClick:s,className:"mb-6 inline-flex cursor-pointer items-center gap-1.5 text-sm text-muted-foreground",children:[(0,t.jsx)(n.ArrowLeft,{className:"size-3"}),(0,t.jsx)("span",{children:"Skills"})]}),(0,t.jsxs)("div",{className:"mb-2",children:[(0,t.jsx)("h1",{className:"m-0 text-[28px] font-normal leading-tight text-foreground",children:e.name}),e.description&&(0,t.jsx)("p",{className:"mb-0 ml-0 mr-0 mt-2 text-sm leading-relaxed text-muted-foreground",children:e.description})]}),(0,t.jsx)("div",{className:"mb-7 mt-6 border-b border-border",children:(0,t.jsx)("div",{className:"flex",children:[{key:"overview",label:"Overview"},{key:"usage",label:"How to Use"}].map(e=>(0,t.jsx)("div",{onClick:()=>u(e.key),className:(0,a.cn)("-mb-px cursor-pointer border-b-[3px] px-5 py-3 text-sm",l===e.key?"border-info font-medium text-info":"border-transparent font-normal text-muted-foreground"),children:e.label},e.key))})}),"overview"===l&&(0,t.jsxs)("div",{className:"flex gap-16",children:[(0,t.jsxs)("div",{className:"min-w-0 flex-1",children:[(0,t.jsx)("h2",{className:"m-0 mb-1 text-lg font-normal text-foreground",children:"Skill Details"}),(0,t.jsx)("p",{className:"m-0 mb-4 text-[13px] text-muted-foreground",children:"Metadata registered with this skill"}),(0,t.jsxs)("table",{className:"w-full border-collapse text-sm",children:[(0,t.jsx)("thead",{children:(0,t.jsxs)("tr",{className:"border-b border-border",children:[(0,t.jsx)("th",{className:"w-40 py-3 text-left font-medium text-muted-foreground",children:"Property"}),(0,t.jsx)("th",{className:"py-3 text-left font-medium text-muted-foreground",children:e.name})]})}),(0,t.jsx)("tbody",{children:m.map((e,r)=>(0,t.jsxs)("tr",{className:"border-b border-border",children:[(0,t.jsx)("td",{className:"py-3 text-foreground",children:e.property}),(0,t.jsx)("td",{className:"py-3 text-foreground",children:e.value})]},r))})]})]}),(0,t.jsxs)("div",{className:"w-60 shrink-0",children:[(0,t.jsxs)("div",{className:"mb-6",children:[(0,t.jsx)("div",{className:"mb-1 text-xs text-muted-foreground",children:"Status"}),(0,t.jsx)("span",{className:(0,a.cn)("rounded-xl px-2.5 py-[3px] text-xs font-medium",e.enabled?"bg-success/10 text-success":"bg-muted text-muted-foreground"),children:e.enabled?"Public":"Draft"})]}),(0,t.jsx)(N,{source:e.source}),e.keywords&&e.keywords.length>0&&(0,t.jsxs)("div",{className:"mb-6",children:[(0,t.jsx)("div",{className:"mb-2 text-xs text-muted-foreground",children:"Tags"}),(0,t.jsx)("div",{className:"flex flex-wrap gap-1.5",children:e.keywords.map(e=>(0,t.jsx)("span",{className:"rounded-2xl border border-border bg-card px-3 py-1 text-xs text-foreground",children:e},e))})]}),(0,t.jsxs)("div",{children:[(0,t.jsx)("div",{className:"mb-1 text-xs text-muted-foreground",children:"Skill ID"}),(0,t.jsx)("div",{className:"break-all font-mono text-xs text-foreground",children:e.id})]})]})]}),"usage"===l&&(0,t.jsxs)("div",{className:"max-w-[640px]",children:[(0,t.jsx)("h2",{className:"m-0 mb-2 text-lg font-normal text-foreground",children:"Using this skill"}),(0,t.jsx)("p",{className:"m-0 mb-6 text-sm leading-relaxed text-muted-foreground",children:"Once your proxy is set as a marketplace, enable this skill in Claude Code with one command:"}),(0,t.jsxs)("div",{className:"mb-6 overflow-hidden rounded-lg border border-border",children:[(0,t.jsxs)("div",{className:"flex items-center justify-between border-b border-border bg-muted px-4 py-2.5",children:[(0,t.jsx)("span",{className:"text-[13px] font-medium text-foreground",children:"Run in Claude Code"}),(0,t.jsxs)("button",{onClick:()=>p(h,"install"),className:(0,a.cn)("flex cursor-pointer items-center gap-1 border-none bg-transparent p-0 text-xs","install"===c?"text-success":"text-info"),children:["install"===c?(0,t.jsx)(o.Check,{className:"size-3"}):(0,t.jsx)(i.Copy,{className:"size-3"}),"install"===c?"Copied":"Copy"]})]}),(0,t.jsx)("pre",{className:"m-0 bg-card px-4 py-3.5 font-mono text-sm text-foreground",children:h})]}),(0,t.jsxs)("div",{className:"mb-4 rounded-lg border border-warning/30 bg-warning/10 px-4 py-3",children:[(0,t.jsxs)("p",{className:"m-0 mb-2 text-[13px] leading-relaxed text-muted-foreground",children:['If you see "Plugin ',e.name,' not found in marketplace", update the catalog first:']}),(0,t.jsx)("pre",{className:"m-0 bg-transparent font-mono text-[13px] text-foreground",children:"/plugin marketplace update litellm"})]}),(0,t.jsxs)("p",{className:"m-0 text-[13px] leading-relaxed text-muted-foreground",children:["Don't have the marketplace configured yet?"," ",(0,t.jsx)("span",{onClick:()=>u("setup"),className:"cursor-pointer text-info",children:"See one-time setup →"})]})]}),"setup"===l&&(0,t.jsxs)("div",{className:"max-w-[640px]",children:[(0,t.jsx)("h2",{className:"m-0 mb-2 text-lg font-normal text-foreground",children:"One-time marketplace setup"}),(0,t.jsx)("p",{className:"m-0 mb-3 text-sm leading-relaxed text-muted-foreground",children:"Run this command in Claude Code to register the marketplace:"}),(0,t.jsxs)("div",{className:"mb-6 overflow-hidden rounded-lg border border-border",children:[(0,t.jsxs)("div",{className:"flex items-center justify-between border-b border-border bg-muted px-4 py-2.5",children:[(0,t.jsx)("span",{className:"text-[13px] font-medium text-foreground",children:"Run in Claude Code"}),(0,t.jsxs)("button",{onClick:()=>{let e=window.location.origin;p(`/plugin marketplace add ${e}/claude-code/marketplace.json`,"marketplace-cmd")},className:(0,a.cn)("flex cursor-pointer items-center gap-1 border-none bg-transparent p-0 text-xs","marketplace-cmd"===c?"text-success":"text-info"),children:["marketplace-cmd"===c?(0,t.jsx)(o.Check,{className:"size-3"}):(0,t.jsx)(i.Copy,{className:"size-3"}),"marketplace-cmd"===c?"Copied":"Copy"]})]}),(0,t.jsx)("pre",{className:"m-0 bg-card px-4 py-3.5 font-mono text-[13px] text-foreground",children:`/plugin marketplace add ${window.location.origin}/claude-code/marketplace.json`})]}),(0,t.jsxs)("p",{className:"m-0 mb-3 text-sm leading-relaxed text-muted-foreground",children:["Or add this to ",(0,t.jsx)("code",{className:"rounded bg-muted px-1.5 py-px text-[13px]",children:"~/.claude/settings.json"})," ","for a persistent configuration:"]}),(0,t.jsxs)("div",{className:"overflow-hidden rounded-lg border border-border",children:[(0,t.jsxs)("div",{className:"flex items-center justify-between border-b border-border bg-muted px-4 py-2.5",children:[(0,t.jsx)("span",{className:"text-[13px] font-medium text-foreground",children:"~/.claude/settings.json"}),(0,t.jsxs)("button",{onClick:()=>p(g,"settings"),className:(0,a.cn)("flex cursor-pointer items-center gap-1 border-none bg-transparent p-0 text-xs","settings"===c?"text-success":"text-info"),children:["settings"===c?(0,t.jsx)(o.Check,{className:"size-3"}):(0,t.jsx)(i.Copy,{className:"size-3"}),"settings"===c?"Copied":"Copy"]})]}),(0,t.jsx)("pre",{className:"m-0 bg-card px-4 py-3.5 font-mono text-[13px] text-foreground",children:g})]})]})]})}],652272)},902555,e=>{"use strict";var t=e.i(843476),r=e.i(746798),n=e.i(271645);let o=n.forwardRef(function(e,t){return n.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:t},e),n.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"}))}),i=n.forwardRef(function(e,t){return n.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:t},e),n.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"}),n.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M21 12a9 9 0 11-18 0 9 9 0 0118 0z"}))});var s=e.i(278587),a=e.i(68155),l=e.i(360820),u=e.i(871943),c=e.i(434626);let d=n.forwardRef(function(e,t){return n.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:2,stroke:"currentColor","aria-hidden":"true",ref:t},e),n.createElement("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"}))});var p=e.i(196631);function h({icon:e,onClick:r,className:n,disabled:o,dataTestId:i}){return o?(0,t.jsx)("span",{className:"inline-flex shrink-0 cursor-not-allowed items-center justify-center p-1.5 opacity-50","data-testid":i,children:(0,t.jsx)(e,{className:"size-5 shrink-0"})}):(0,t.jsx)("span",{className:(0,p.cx)("inline-flex shrink-0 cursor-pointer items-center justify-center p-1.5",n),onClick:r,"data-testid":i,children:(0,t.jsx)(e,{className:"size-5 shrink-0"})})}let g={Edit:{icon:o,className:"hover:text-info"},Delete:{icon:a.TrashIcon,className:"hover:text-destructive"},Test:{icon:i,className:"hover:text-info"},Regenerate:{icon:s.RefreshIcon,className:"hover:text-success"},Reset:{icon:s.RefreshIcon,className:"hover:text-info"},Up:{icon:l.ChevronUpIcon,className:"hover:text-info"},Down:{icon:u.ChevronDownIcon,className:"hover:text-info"},Open:{icon:c.ExternalLinkIcon,className:"hover:text-success"},Copy:{icon:d,className:"hover:text-info"}};e.s(["default",0,function({onClick:e,tooltipText:n,disabled:o=!1,disabledTooltipText:i,dataTestId:s,variant:a}){let{icon:l,className:u}=g[a],c=o?i:n,d=(0,t.jsx)(h,{icon:l,onClick:e,className:u,disabled:o,dataTestId:s});return c?(0,t.jsx)(r.TooltipProvider,{children:(0,t.jsxs)(r.Tooltip,{children:[(0,t.jsx)(r.TooltipTrigger,{render:(0,t.jsx)("span",{tabIndex:o?0:void 0}),children:d}),(0,t.jsx)(r.TooltipContent,{children:c})]})}):(0,t.jsx)("span",{children:d})}],902555)},292335,e=>{"use strict";let t={NONE:"none",API_KEY:"api_key",BEARER_TOKEN:"bearer_token",TOKEN:"token",BASIC:"basic",OAUTH2:"oauth2",OAUTH2_TOKEN_EXCHANGE:"oauth2_token_exchange",OAUTH2_ID_JAG:"oauth2_id_jag",AWS_SIGV4:"aws_sigv4",TRUE_PASSTHROUGH:"true_passthrough",OAUTH_DELEGATE:"oauth_delegate"},r=[{value:t.NONE,label:"None"},{value:t.API_KEY,label:"API Key"},{value:t.BEARER_TOKEN,label:"Bearer Token"},{value:t.TOKEN,label:"Token"},{value:t.BASIC,label:"Basic Auth"},{value:t.OAUTH2,label:"OAuth"},{value:t.OAUTH2_TOKEN_EXCHANGE,label:"OAuth Token Exchange (OBO)"},{value:t.OAUTH2_ID_JAG,label:"ID-JAG (Okta Cross App Access)"},{value:t.AWS_SIGV4,label:"AWS SigV4 (Bedrock AgentCore MCPs)"},{value:t.TRUE_PASSTHROUGH,label:"True Passthrough (no Waypoint auth)"},{value:t.OAUTH_DELEGATE,label:"OAuth Delegate (client-supplied upstream token)"}],n=e=>e===t.TRUE_PASSTHROUGH||e===t.OAUTH_DELEGATE,o={INTERACTIVE:"interactive",M2M:"m2m"},i=e=>{let t=e.credentials??{};return JSON.stringify({url:"string"==typeof e.url?e.url:null,spec_path:"string"==typeof e.spec_path?e.spec_path:null,auth_type:e.auth_type??null,oauth_flow_type:e.oauth_flow_type??null,client_id:t.client_id??null,client_secret:t.client_secret??null,scopes:t.scopes??null,upstream_resource:t.upstream_resource??null,issuer:e.issuer??null,authorization_url:e.authorization_url??null,token_url:e.token_url??null,registration_url:e.registration_url??null})},s=["client_id","client_secret"],a=["upstream_resource","upstream_token_header"],l=["access_token","refresh_token","expires_in","scope"],u=(e,t)=>{if(!e)return;let r=Object.fromEntries(t.filter(t=>"string"==typeof e[t]&&""!==e[t]).map(t=>[t,e[t]]));return Object.keys(r).length>0?r:void 0},c="client_credentials",d={SSE:"sse",HTTP:"http",STDIO:"stdio",OPENAPI:"openapi"},p=[{value:d.HTTP,label:"Streamable HTTP (Recommended)"},{value:d.SSE,label:"Server-Sent Events (SSE)"},{value:d.STDIO,label:"Standard Input/Output (stdio)"},{value:d.OPENAPI,label:"OpenAPI Spec"}];e.s(["ADMIN_CONFIG_CREDENTIAL_KEYS",0,a,"AUTH_TYPE",0,t,"AUTH_TYPE_ITEMS",0,r,"CLEARED_ON_INVALIDATION",0,["credentials"],"MCP_OAUTH2_FLOW_INTERACTIVE",0,"authorization_code","MCP_OAUTH2_FLOW_M2M",0,c,"MCP_REACHABLE_DESCRIPTION",0,"Server responded. Authentication and tools were not checked","OAUTH_FLOW",0,o,"TRANSPORT",0,d,"TRANSPORT_ITEMS",0,p,"credentialAuthClass",0,e=>e===t.TRUE_PASSTHROUGH||e===t.OAUTH_DELEGATE?"client_forwarded":e??null,"gatewayMintsClientFor",0,e=>e.auth_type===t.TRUE_PASSTHROUGH||e.auth_type===t.OAUTH_DELEGATE&&!e.dcr_bridge,"getMcpOAuthMode",0,function(e){return e.auth_type===t.OAUTH2_TOKEN_EXCHANGE?"token_exchange":e.auth_type!==t.OAUTH2?null:e.oauth2_flow===c?"m2m":e.delegate_auth_to_upstream?"passthrough":"authorization_code"},"getOAuthAuthorizationIdentity",0,i,"handleAuth",0,e=>null==e?t.NONE:e,"handleTransport",0,(e,t)=>null==e?d.SSE:t&&e!==d.STDIO?d.OPENAPI:e,"isClientForwardedTokenMode",0,n,"isHeldOAuthTokenStale",0,(e,t)=>void 0!==t&&i(e)!==t,"isUnsupportedOnGatewayConnect",0,e=>n(e)||e===t.OAUTH2_TOKEN_EXCHANGE,"oauth2FlowToFormValue",0,function(e){return e===c?o.M2M:e?o.INTERACTIVE:void 0},"preservedAdminCredentials",0,e=>u(e,[...s,...a]),"preservedDeclaredAppCredentials",0,e=>u(e,s),"withoutMintedTokenCredentials",0,e=>{if(!e)return;let t=Object.fromEntries(Object.entries(e).filter(([e])=>!l.includes(e)));return Object.keys(t).length>0?t:void 0}])},845150,e=>{"use strict";var t=e.i(843476),r=e.i(271645),n=e.i(131792);let o=(e,t)=>{let r=t.trim().toLowerCase();return!r||e.label.toLowerCase().includes(r)||e.value.toLowerCase().includes(r)||(e.description?.toLowerCase().includes(r)??!1)};e.s(["MultiSelect",0,function({id:e,options:i,value:s=[],onValueChange:a,placeholder:l="Select options",emptyText:u="No options found",disabled:c=!1,loading:d=!1,allowCustomValues:p=!1,className:h}){let g=(0,n.useComboboxAnchor)(),[m,b]=(0,r.useState)(""),f=i.filter(e=>null!=e&&"string"==typeof e.value&&e.value.length>0),v=s.filter(e=>"string"==typeof e&&e.length>0).map(e=>f.find(t=>t.value===e)??{label:e,value:e}),x=m.trim(),k=f.some(e=>e.value.toLowerCase()===x.toLowerCase()),_=p&&x&&!k?[...f,{label:`Create "${x}"`,value:x}]:f;return(0,t.jsxs)(n.Combobox,{multiple:!0,items:_,value:v,onValueChange:e=>{a(Array.from(new Set(p?e.flatMap(e=>s.includes(e.value)?[e.value]:e.value.split(",").map(e=>e.trim()).filter(e=>e.length>0)):e.map(e=>e.value)))),b("")},inputValue:m,onInputValueChange:b,isItemEqualToValue:(e,t)=>e.value===t.value,itemToStringLabel:e=>e.label,filter:o,disabled:c||d,children:[(0,t.jsx)(n.ComboboxChips,{render:(0,t.jsx)("div",{ref:g}),className:`min-h-8 py-1 text-sm ${h??""}`,children:(0,t.jsx)(n.ComboboxValue,{children:r=>(0,t.jsxs)(t.Fragment,{children:[r.map(e=>(0,t.jsx)(n.ComboboxChip,{"aria-label":e.label,children:e.label},e.value)),(0,t.jsx)(n.ComboboxChipsInput,{id:e,placeholder:d?"Loading...":l,className:"min-w-24","aria-label":l||void 0}),r.length>0&&!c&&!d&&(0,t.jsx)(n.ComboboxClear,{className:"ml-auto self-center","aria-label":"Clear all"})]})})}),(0,t.jsxs)(n.ComboboxContent,{anchor:g,children:[(0,t.jsx)(n.ComboboxEmpty,{children:u}),(0,t.jsx)(n.ComboboxList,{children:e=>(0,t.jsx)(n.ComboboxItem,{value:e,disabled:e.disabled,children:(0,t.jsxs)("span",{className:"min-w-0",children:[(0,t.jsx)("span",{className:"block truncate",children:e.label}),e.description&&(0,t.jsx)("span",{className:"block truncate text-xs text-muted-foreground",children:e.description})]})},e.value)})]})]})}])},741466,e=>{"use strict";e.s(["DEBOUNCE_WAIT_MS",0,300])},899426,e=>{"use strict";let t=e=>e.trim().toLowerCase();function r(e,r){let n=t(e);if(""===n)return!0;let o=r.filter(e=>"string"==typeof e).map(e=>e.toLowerCase());return!!o.some(e=>e.includes(n))||n.split(/\s+/).every(e=>o.some(t=>t.includes(e)))}e.s(["filterBySearchTerm",0,function(e,t,n){return e.filter(e=>r(t,n(e)))},"matchesSearchTerm",0,r,"rankBySearchRelevance",0,function(e,r,n){let o=t(r);if(""===o)return[...e];let i=e=>{let t=n(e).toLowerCase();return 1e3*(t===o)+100*!!t.startsWith(o)+(1e3-t.length)};return[...e].sort((e,t)=>i(t)-i(e))}])}]);