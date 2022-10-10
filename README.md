# ssof-automation

## Overview

Apache Airflow serves a multitude of purposes. Here, I explore and experiment with its different features (old and new), usecases, and implementation styles in order to help cement my understanding and familiarity of the toolset and its extensibility. 

## What I Would Do Differently

The start of this learning process began with a hyper-focus on one particular use case I found interesting-- automating vulnerability updates, checking against existing products and services, and adding to a db. However, I felt compelled to use this to additionally explore further a particular interest of mine called RDF Stores. RDF Stores are a way to semantically store and query data in a remarkably flexible way. Though, with these combined domains, both of which I am learning (and would like to continue learning), I found that embedding a technology you would like to learn inside of learning about another technology can be an intense and somewhat disorienting endeavor. I've been told that I'm a big-picture person, and I got lost in a vague larger picture. 

I believe I also misprioritized important but auxillary libraries and implementation details. I wanted to learn the ins-and-outs of Alpine, understand why it's considered so secure, and push through building made-from-scratch images for Airflow all while considering network trouble-shooting within those containers, CI/CD, and other tasks that, however easy or achievable, were simply contributing to the fog of a lack of direction.

If done again, I would start as small as possible and build-up, rather than conjure up a grandiose usecase to work through in just a week. All of that being said! I learned a whole lot.

## What I've Learned and Where I Am Now

The architecture, language, and modularity of Airflow and DockerOperators are becoming increasingly intuitive to me. I feel I'm aware of what I don't know while knowing how to find the answers, whether through a few quick searches or by asking a colleague. I am always willing to ask a colleague for guidance and have enough effort and enthusiasm to give to become a 

I can fill in most of my gaps in knowledge and experience. With direction and internal feedback, I'm far more than confident in my ability to claim proper ownership of these tools and skillsets in minimal time. I am strongly motivated and willing to put in the time and effort to become a powerful contributer to the SS&C team My interest in the tooling, its modularity, and its applications is high and only growing, and my willingness to put in the time and elbow-grease to be a powerful contributer to the SS&C team  

## What I would do differently... (if given this time again...)

## Where I feel I can improve...

## Overall Experience

### Difficulties in learning with assumed use cases. 

- i like to be big picture but also strive to be a better overall engineer

### NVD Client

- impl architecture is restricted by use case knowledge (i.e. how it will be used in automation (e.g. how info will be passed in)) and knowledge of python. 

## Codebase Background

This codebase began with a hyper-focus on one particular use case I found interesting-- automating vulnerability updates, checking against existing products and services, and adding to a db. Additionally, I wanted to explore adding a particular interest of mine called RDF Stores. RDF Stores are a way to semantically store and query data in a remarkably flexible way. However, with this entire approach, I found that both some of my domain knowledge needed guidance and the vulnerability apis of choice are time intensive to fully implement-- PLUS RDF setup (example ontology creation, and triple store init, THEN setting up an api).

### DAGs You Will Find

- update vulns
-

## Context

Data pipelining tools offer a lot of flexibility but have trouble merging disparate data sources and gaining data insight from successfully doing so. The more data sources you have, the more difficult and resource intensive it is to merge.

### Additional Context Considerations

This project, at least at the moment, is primarily for the purposes of learning, showing competency of, apache airflow and related technologies while exploring prior unexplored domains and tooling in the InfoSec space.

## Would love to continue some of these builds

### WORKFLOW of main interest

- create hub and spoke onto architecture
- create ontos for apis
- connect retrieved data through ontos in triplestore

### APIs of Interest

<!-- <https://github.com/jaegeral/security-apis> -->

## Offered Solution

Brief: RDF is a specification for a simple data model that consists only of a Subject, Predicate, and an Object-- e.g:
```<ex:App_Foo> <ex:has_software_dependency> <ex:Log4J_v1.2>```
where 'ex:' is a namespace specifier. The three-part model allows for rigid ontological and topological constraints in the form of first order logic axioms. These constrants ensure that the model is correct. Though more importantly, the constraints ensure the model has semantic value that can be explored and analyzed with tremendous depth. Thus, it is worth harnessing the power of both more commonly used data stores in parallel with RDF stores (also referred to as Triple Stores) anywhere one might need to merge, analyze, and flexibly query large amounts of data.

Companies leveraging semantic data technologies into their data workflows and discovery processes...

Despite how quickly technologies can evolve within company, an organization very often becomes and remains somewhat tunnel-visioned on the technical progress itself while unknowingly bound to the tools and processes already in place, even when these tools and processes in one way or another revolve around flexibility, embracing change, rapid development, things of the like. The practices, and procedures imposed on our approach to data in rapidly moving environments often impose a structure that is stubborn in its direction and rigid in its space. In stronger words, it is largely, and likely somewhat globally, habitually underappreciate the extent to which our handling of, interpretation of, and synthesis with data influences and affects decision-making in countless domains. Perhaps not by some astronomical amount, but certianly by an highly non-negligible amount. The tools companies have come to use to deal with data aims, on the whole, to serve only efficiency and velocity while giving an exaggerated notion of insight, meaning, and value through [adj] solutions. Above all, notions of any topological relationship between data, insight, and knowledge gets buried considerably in the backlog.

## Conditions that SHOULD to be met

<!-- A recognition that data often has more semantic value before it rockets into processing and interpretation land is the launchpad for any discussion on or demonstration of how to  -->
A solution is not being proposed ...
"Solutions" to this relationship are not radical alternatives to any current tool chain. They  They are simply foundations on which these things can operate.It is neither new nor niche, just not realized to its full potential in many domains.

Companies, institutions, people spend lots of time and effort gathering and structuring somewhat reliable data, and the methods we decide to employ in order to wrangle it largely go against what information lies in their original structure.

- plethora of structured, and semi-structured data
- silo'd

## -

Serve as a great example of what kind of models can come out of such a strong bedding.

- NVD's and MITRE's datasets interested me in their interoperability (in obvious addition to sheer size).

As someone who wants to learn, I prefer tinkering myself

- massive amounts of data
- similarly structured
- similar domains
- makes it an easy candidate for graph processing*

To notify, inform solutions, to build off of.

## Goals

- Data Enrichment
- Easier manual and automated semantic navigation of large datasets
- Business Continuity
- Increase operational efficiency

## Conditions that Need to Be Met

## Mini WBS

1. [ ] Create single api dag run

## TODOs

- [ ] Reformat CVE Documentation
  - Will act as better baseline for future api/service client documentation
- [ ] Add functionality to keep track of latest NVD CVE/CPE request
  - This will allow future requests to autopopulate with data that has been updated since.

### Technologies

Semantic Data, REST APIs

## Service / Workflow Architectural Components

The core of this app, as is the core of a behemoth multitude of workflow automation apps and services, is Apache Airflow.

- Particularly in infosec and security automation
  1. Centralized workflow and logging
- giving way to centralized monitoring, efficient observability and monitoring.

## Package structure

While conceptualizing, prototyping, and iterating over any solution implementations within a given problem-space, the simplest implementations are often most self-advised. This way, I can focus on a larger idea without losing bandwidth in any attemps to perfect some component implementation.

### Questions

- why "wordkflows" instead of tasks?

### Ontologies

#### Keywords

### Meta

#### What I Would Have Done Differently
