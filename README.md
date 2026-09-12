# Kubernetes + AI/ML Infrastructure Portfolio

A set of hands-on projects exploring how machine learning and LLM workloads are
built, served, and orchestrated on Kubernetes — combining Kubernetes administration
fundamentals with modern MLOps and LLMOps practices.

## Projects

### 1. [ML Model Serving on Kubernetes](./ml-on-k8s) — manual deployment

Trained a scikit-learn model, wrapped it in a FastAPI service, containerized it,
and deployed it to Kubernetes by hand — Deployment, Service, readiness probes,
resource limits, and observed self-healing via the Deployment controller.

**Demonstrates:** core Kubernetes administration — Deployments, Services, health
checks, resource management, container image workflows for local clusters (kind).

### 2. [Model Serving with KServe](./ml-on-k8s#model-serving-with-kserve) — managed inference platform

Deployed the same model through KServe, comparing a hand-written deployment against
a Kubernetes-native model-serving framework — standardized inference API, Istio
ingress routing, and Knative-based autoscaling infrastructure, backed by a
PersistentVolumeClaim for custom model storage.

**Demonstrates:** model-serving frameworks, service mesh (Istio), serverless
scaling primitives (Knative), and the tradeoffs between manual and managed
deployment approaches.

### 3. [RAG Pipeline on Kubernetes](./rag-on-k8s) — LLM infrastructure

Built a full retrieval-augmented generation system running entirely in-cluster:
Qdrant for vector storage, Ollama for embeddings and generation (CPU-only, no GPU
required), and a FastAPI service tying retrieval and generation together —
communicating over Kubernetes service DNS.

**Demonstrates:** LLM serving infrastructure, vector databases, multi-service
orchestration, and the specific operational challenges of running AI workloads
on Kubernetes (resource contention, service discovery, debugging distributed
systems).

## Why these three together

Each project intentionally builds on a different layer of the stack:

| Layer | Project | Key skill |
|---|---|---|
| Foundation | Manual deployment | Kubernetes primitives |
| Framework | KServe | Standardized model serving at scale |
| Application | RAG pipeline | End-to-end AI system design |

Together they cover the practical range of what a Platform/MLOps engineer is
expected to know: deploying a model by hand, using the frameworks that make
that easier at scale, and building the kind of AI-native application
(RAG/LLM-based) that's now common in production.

## Environment

All projects were built and tested on a local `kind` Kubernetes cluster
(single-node), intentionally chosen to keep the focus on Kubernetes/MLOps
concepts rather than cloud provider setup. Notes on adapting each to a
cloud-managed cluster (GKE/EKS/AKS) are included in the individual project
READMEs where relevant.

## Real issues encountered (and why they're included)

Debugging notes are kept in each project's README rather than smoothed over,
since diagnosing real failures — resource contention, service-to-service
networking, port conflicts, storage lifecycle issues — is a more accurate
signal of practical Kubernetes experience than a clean, unbroken walkthrough.
