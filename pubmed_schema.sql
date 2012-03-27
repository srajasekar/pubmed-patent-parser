-- author : ajbharani
-- author : saran
-- pubmed_Article(Id, Abstract, Body)
create table pubmed_Article(
    Id integer not null auto_increment,
    ArticleIds long varchar,
    ArticleKeywords long varchar,
    Abstract long varchar,
    Body long varchar,
    PubDate Date,
    Deleted integer not null default 0,
    constraint ARTPK1 primary key(Id)
);

-- pubmed_Keyword(ArticleId, Keyword)
create table pubmed_Keyword (
    ArticleId integer not null,
    Keyword long varchar not null,
    constraint KWDFK1 foreign key(ArticleId) references pubmed_Article(Id)
);

-- pubmed_Title(ArtilceId, Title)
create table pubmed_Title (
    ArticleId integer not null,
    Title long varchar,
    constraint TITFK1 foreign key(ArticleId) references pubmed_Article(Id)
);

-- pubmed_Contributor(ArtilceId, ContribType, Surname, GivenNames)
create table pubmed_Contributor (
    ArticleId integer not null,
    ContribType varchar(2048),
    Surname varchar(2048),
    GivenNames varchar(2048),
    constraint CONTRIBFK1 foreign key(ArticleId) references pubmed_Article(Id)
);

-- pubmed_Keyword(ArtilceId, Keyword)
create table pubmed_NgramKeyword (
    ArtilceId integer not null,
    NgramKeyword long varchar,
    NgramSize integer,
    TF real,
    IDF real,
    PMI real,
    constraint KWFK1 foreign key(ArtilceId) references pubmed_Article(Id)
);

-- pubmed_Reference(Id, AricleId, RefId, RefType, Source, Title, PubYear, PubIdType, PubId)
create table pubmed_Reference (
    Id integer not null auto_increment,
    ArticleId integer not null,    
    RefId varchar(2048),
    RefType varchar(2048),
    Source varchar(2048),
    Title long varchar,
    PubYear varchar(2048),
    PubIdType varchar(2048),
    PubId varchar(2048),
    constraint REFPK1 primary key(Id),
    constraint REFFK1 foreign key(ArticleId) references pubmed_Article(Id)
);

-- pubmed_RefContributor(Id, ContribType, Surname, GivenNames)
create table pubmed_RefContributor (
    RefId integer not null,
    ContribType varchar(2048),
    Surname varchar(2048),
    GivenNames varchar(2048),
    constraint REFCONTRIBFK1 foreign key(RefId) references pubmed_Reference(Id)
);