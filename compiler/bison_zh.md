- [Bison 3.8.1](#bison-381)
- [介绍](#介绍)
- [Bison使用条件](#bison使用条件)
- [GNU通用公共许可证](#gnu通用公共许可证)
  - [前言](#前言)
  - [条款与条件](#条款与条件)
- [如何将这些条款应用于您的新计划](#如何将这些条款应用于您的新计划)
- [3 Bison Grammar Files](#3-bison-grammar-files)
  - [3.1 Outline of a Bison Grammar](#31-outline-of-a-bison-grammar)
    - [3.1.1 The prologue](#311-the-prologue)
    - [3.1.2 Prologue Alternatives](#312-prologue-alternatives)
    - [3.1.3 The Bison Declarations Section](#313-the-bison-declarations-section)
    - [3.1.4 The Grammar Rules Section](#314-the-grammar-rules-section)
    - [3.1.5 The epilogue](#315-the-epilogue)
  - [3.2 Symbols, Terminal and Nonterminal](#32-symbols-terminal-and-nonterminal)
  - [3.3 Grammar Rules](#33-grammar-rules)
    - [3.3.1 Syntax of Grammar Rules](#331-syntax-of-grammar-rules)
    - [3.3.2 Empty Rules](#332-empty-rules)
    - [3.3.3 Recursive Rules](#333-recursive-rules)
  - [3.4 Defining Language Semantics](#34-defining-language-semantics)
    - [3.4.1 Data Types of Semantic Values](#341-data-types-of-semantic-values)
    - [3.4.2 More Than One Value Type](#342-more-than-one-value-type)
    - [3.4.3 Generating the Semantic Value Type](#343-generating-the-semantic-value-type)
    - [3.4.4 The Union Declaration](#344-the-union-declaration)
    - [3.4.5 Providing a Structured Semantic Value Type](#345-providing-a-structured-semantic-value-type)
    - [3.4.6 Actions](#346-actions)
    - [3.4.7 Data Types of Values in Actions](#347-data-types-of-values-in-actions)
    - [3.4.8 Actions in Midrule](#348-actions-in-midrule)
      - [3.4.8.1 Using Midrule Actions](#3481-using-midrule-actions)
      - [Typed Midrule Actions](#typed-midrule-actions)
      - [3.4.8.3 Midrule Action Translation](#3483-midrule-action-translation)
      - [3.4.8.4 Conflicts due to Midrule Actions](#3484-conflicts-due-to-midrule-actions)
  - [3.5 Tracking Locations](#35-tracking-locations)
    - [3.5.1 Data Type of Locations](#351-data-type-of-locations)
    - [3.5.2 Actions and Locations](#352-actions-and-locations)
    - [3.5.3 Printing Locations](#353-printing-locations)
    - [3.5.4 Default Action for Locations](#354-default-action-for-locations)
  - [3.6 Named References](#36-named-references)
  - [3.7 Bison Declarations](#37-bison-declarations)
    - [3.7.1 Require a Version of Bison](#371-require-a-version-of-bison)
    - [3.7.2 Token Kind Names](#372-token-kind-names)
    - [3.7.3 Operator Precedence](#373-operator-precedence)
    - [3.7.4 Nonterminal Symbols](#374-nonterminal-symbols)
    - [3.7.5 Syntax of Symbol Declarations](#375-syntax-of-symbol-declarations)
    - [3.7.6 Performing Actions before Parsing](#376-performing-actions-before-parsing)
    - [3.7.7 Freeing Discarded Symbols](#377-freeing-discarded-symbols)
    - [3.7.8 Printing Semantic Values](#378-printing-semantic-values)
    - [3.7.9 Suppressing Conflict Warnings](#379-suppressing-conflict-warnings)
    - [3.7.10 The Start-Symbol](#3710-the-start-symbol)
    - [3.7.11 A Pure (Reentrant) Parser](#3711-a-pure-reentrant-parser)
    - [3.7.12 A Push Parser](#3712-a-push-parser)
    - [3.7.13 Bison Declaration Summary](#3713-bison-declaration-summary)
    - [3.7.14 %define Summary](#3714-define-summary)
    - [3.7.15 %code Summary](#3715-code-summary)
- [4 Parser C-Language Interface](#4-parser-c-language-interface)
  - [4.1 The Parser Function yyparse](#41-the-parser-function-yyparse)
  - [4.5 Special Features for Use in Actions](#45-special-features-for-use-in-actions)


# Bison 3.8.1
本手册（2021年9月10日）适用于GNU Bison（版本3.8.1），GNU解析器生成器。

版权所有© 1988–1993、1995、1998–2015、2018–2021自由软件基金会，Inc。

根据GNU自由文档许可证第1.3版或自由软件基金会后续发布的任何版本的条款，允许复制、分发和/或修改本文档，没有不变的部分，前封面文字为“A GNU Manual”，后封面文字如下（a）。许可证的副本包含在名为“GNU自由文档许可证”的部分中。
```
（a）FSF的后封面文字是：“您有自由复制和修改此GNU手册。从FSF购买的副本支持其开发GNU和促进软件自由。”
``````
# 介绍
Bison是一款通用的解析器生成器，它将带有注释的上下文无关文法转换为确定性的LR或广义LR（GLR）解析器，采用LALR(1)、IELR(1)或规范LR(1)解析器表。一旦您熟练掌握了Bison，您就可以使用它开发各种语言解析器，从用于简单台式计算器到复杂编程语言的解析器都可以实现。

Bison与Yacc向上兼容：所有正确编写的Yacc文法都应该在Bison上无需更改即可工作。任何熟悉Yacc的人都应该能够毫不费力地使用Bison。要使用Bison或理解本手册，您需要精通C、C++、D或Java编程语言。

我们从教程章节开始，解释了使用Bison的基本概念，并展示了三个已解释的示例，每个示例都在前一个基础上构建。如果您不了解Bison或Yacc，请从阅读这些章节开始。随后是参考章节，详细描述了Bison的特定方面。

Bison最初由Robert Corbett编写。Richard Stallman使其与Yacc兼容。Carnegie Mellon University的Wilfred Hansen添加了多字符字符串文字和其他功能。自那时以来，多亏了众多志愿者的辛勤工作，Bison变得更加强大，并发展出许多其他新功能。有关详细信息，请参阅Bison发行版中包含的THANKS和ChangeLog文件。

本版本对应于Bison的3.8.1版本。

# Bison使用条件
Bison生成的解析器的分发条款允许在非自由软件中使用这些解析器。在Bison版本2.2之前，这些额外的权限仅适用于Bison生成的C中的LALR(1)解析器。而在Bison版本1.24之前，Bison生成的解析器只能在自由软件程序中使用。

其他GNU编程工具，如GNU C编译器，从来没有这种要求。它们一直可以用于非自由软件。Bison不同的原因并不是由于特殊的政策决定；而是由于将通常的通用公共许可证应用于Bison所有源代码。

Bison工具的主要输出——Bison解析器实现文件——包含Bison的一个相当大的部分的文字副本，这部分是解析器实现的代码。（您的文法中的操作被插入到此实现的某一点，但大多数实现的其余部分没有更改。）当我们将GPL条款应用于解析器实现的骨架代码时，其效果是限制了Bison输出的使用仅限于自由软件。

我们没有改变这些条款是因为对于希望将软件变为专有的人们表示同情。软件应该是自由的。但我们得出结论，将Bison的使用限制为自由软件对鼓励人们将其他软件变为自由软件的做法作用有限。因此，我们决定使使用Bison的实际条件与使用其他GNU工具的实际条件相匹配。

此异常适用于Bison生成解析器代码的情况。您可以通过检查Bison输出文件以查看以“特殊例外…”开头的文本来确定是否适用此异常。文本详细说明了异常的确切条款。

# GNU通用公共许可证
版本3，2007年6月29日

版权所有 © 2007 自由软件基金会 https://fsf.org/

任何人都有权复制和分发本许可证文档的文字副本，但不允许对其进行修改。
## 前言
GNU通用公共许可证是一种用于软件和其他类型作品的自由、版权保护的许可证。

大多数软件和其他实用作品的许可证旨在剥夺您分享和更改这些作品的自由。相反，GNU通用公共许可证旨在保证您分享和更改程序的所有版本的自由，以确保它对所有用户保持自由软件。我们，自由软件基金会，对大部分我们的软件使用GNU通用公共许可证；它也适用于任何其他以这种方式发布的作品。您也可以将其应用于您的程序。

当我们谈论自由软件时，我们指的是自由，而不是价格。我们的通用公共许可证旨在确保您有权分发自由软件的副本（如果您愿意，还可以对其收费），您可以获取源代码或者如果您需要的话可以获取它，您可以更改软件或者在新的自由程序中使用它的部分，并且您知道您可以执行这些操作。

为了保护您的权利，我们需要阻止其他人剥夺您这些权利或要求您放弃这些权利。因此，如果您分发该软件的副本或者对其进行修改，您有一定的责任来尊重他人的自由。

例如，如果您分发此类程序的副本，无论是免费还是付费，您必须将您获得的相同自由传递给接收者。您必须确保他们也能够获取源代码。并且您必须向他们展示这些条款，以便他们了解他们的权利。

使用GNU GPL的开发人员通过两个步骤保护您的权利：(1) 在软件上声明版权，以及(2) 向您提供此许可证，以便您在法律上获得复制、分发和/或修改它的许可。

出于开发人员和作者的保护考虑，GPL明确解释了这个免费软件没有担保。为了用户和作者的利益，GPL要求标记修改后的版本为已更改，以免将其问题错误地归因于先前版本的作者。

一些设备旨在阻止用户访问在其中运行的软件的修改版本，尽管制造商可以这样做。这与保护用户更改软件自由的目标根本不兼容。这种滥用的系统性模式发生在供个人使用的产品领域，这正是最不可接受的地方。因此，我们设计了GPL的这个版本，以禁止这种做法用于这些产品。如果在其他领域出现类似问题，我们将随时准备在未来的GPL版本中扩展这一规定，以保护用户的自由。

最后，每个程序都不断受到软件专利的威胁。各国不应允许专利限制在通用计算机上的软件开发和使用，但在存在这种情况的国家，我们希望避免专利应用于自由软件可能使其事实上成为专有软件的特殊危险。为了防止这种情况发生，GPL确保专利不能用于使程序成为非自由软件。

具体的复制、分发和修改条款如下。


## 条款与条件
0. **定义。**

“本许可证”是指 GNU 通用公共许可证的第 3 版。

“版权”也指适用于其他类型作品（如半导体掩模）的类似版权的法律。

“本程序”是指根据本许可许可的任何受版权保护的作品。每个被许可人都称呼为“您”。“被许可方”和“接收方”可以是个人或组织。

“修改”作品是指以需要版权许可的方式复制或改编全部或部分作品，而不是制作精确副本。由此产生的作品被称为早期作品的“修改版本”或“基于”早期作品的作品。

“涵盖作品”是指未经修改的程序或基于程序的作品。

“传播”作品是指未经许可对作品进行任何操作，使您根据适用的版权法直接或间接承担侵权责任，但在计算机上执行或修改私人副本除外。传播包括复制、分发（有或没有修改）、向公众提供，在一些国家还包括其他活动。

“传达”作品是指使其他方能够制作或接收复制品的任何传播。仅仅通过计算机网络与用户进行交互，而不传输副本，是没有传达的。

交互式用户界面显示“适当的法律声明”，只要它包括一个方便且醒目的功能，即 （1） 显示适当的版权声明，以及 （2） 告诉用户作品没有保证（除非提供保证），被许可人可以根据本许可转让作品， 以及如何查看本许可证的副本。如果界面显示用户命令或选项的列表（如菜单），则列表中的突出项目符合此条件。

1. **源代码。**

作品的“源代码”是指作品修改的首选形式。“目标代码”是指作品的任何非来源形式。

“标准接口”是指由公认的标准机构定义的官方标准的接口，或者在为特定编程语言指定的接口的情况下，在使用该语言工作的开发人员中广泛使用的接口。

可执行作品的“系统库”包括除整个作品之外的任何内容，这些内容（a）包含在打包主要组件的正常形式中，但不是该主要组件的一部分，以及（b）仅用于使该主要组件的工作能够使用，或实现一个标准接口，该接口的实现以源代码形式向公众开放。在此上下文中，“主要组件”是指运行可执行工作的特定操作系统（如果有）的主要基本组件（内核、窗口系统等），或用于生成工作的编译器，或用于运行它的目标代码解释器。

目标代码形式的作品的“对应源代码”是指生成、安装和（对于可执行作品）运行目标代码和修改作品所需的所有源代码，包括控制这些活动的脚本。但是，它不包括作品的系统库，或通用工具或普遍可用的免费程序，这些程序在执行这些活动时未经修改使用，但不是作品的一部分。例如，“对应源”包括与作品的源文件相关联的接口定义文件，以及作品专门设计需要的共享库和动态链接子程序的源代码，例如通过这些子程序与工作的其他部分之间的密切数据通信或控制流。

对应源不需要包含用户可以从相应源的其他部分自动生成的任何内容。

源代码形式的工作的对应源代码是相同的作品。

2. **基本权限。**

根据本许可授予的所有权利均在程序的版权期限内授予，并且只要满足规定的条件，则不可撤销。本许可明确确认您无限制地运行未经修改的程序。仅当该作品的内容构成涵盖作品时，运行涵盖作品的输出才受本许可保护。本许可承认您的合理使用权或版权法规定的其他等效权利。

您可以制作、运行和传播您不转让的涵盖作品，只要您的许可仍然有效，就可以无条件地进行。您可以将涵盖的作品转让给他人，其唯一目的是让他们专门为您进行修改，或为您提供运行这些作品的设施，前提是您在转让您不控制版权的所有材料时遵守本许可的条款。因此，为您制作或运行所涵盖作品的人必须完全代表您，在您的指导和控制下，其条款禁止他们在与您的关系之外制作您的受版权保护材料的任何副本。

只有在以下条件下，才允许在任何其他情况下进行运输。不允许再许可;第10节规定没有必要。

3. **保护用户的合法权利免受反规避法的侵害。**

根据履行1996年12月20日通过的《世界知识产权组织版权条约》第11条规定的义务的任何适用法律或禁止或限制规避此类措施的类似法律，任何涵盖的作品均不得被视为有效技术措施的一部分。

当您转让涵盖的作品时，您放弃禁止规避技术措施的任何法律权力，只要这种规避是通过行使本许可下对涵盖作品的权利来实现的，并且您否认任何限制作品的操作或修改作为对作品用户强制执行的手段的意图， 您或第三方禁止规避技术措施的合法权利。

4. **逐字传送副本。**

您可以在收到程序源代码时以任何媒介逐字传送副本，前提是您在每个副本上以显眼和适当的方式发布适当的版权声明;保持所有声明本许可和根据第 7 节添加的任何非许可条款适用于本准则的声明不变;保持所有没有任何保证的通知;并向所有接收者提供本许可证的副本以及程序。

您可以对您传达的每份副本收取任何价格或不收取任何价格，并且可以付费提供支持或保修保护。

5. **传达修改后的源码版本。**

根据第 4 节的条款，您可以以源代码的形式传达基于本程序的作品或从本程序生成作品的修改，前提是您还满足以下所有条件：

- 作品必须带有醒目的通知，说明您对其进行了修改，并给出了相关日期。

- 作品必须带有醒目的通知，说明它是根据本许可证和第 7 节添加的任何条件发布的。这项要求修改了第4节中的要求，即“保持所有通知的完整性”。

- 您必须根据本许可将整个作品作为一个整体许可给拥有副本的任何人。因此，本许可连同任何适用的第 7 节附加条款将适用于整个作品及其所有部分，无论它们如何包装。本许可不授予以任何其他方式许可作品的许可，但如果您单独收到该许可，则不会使此类许可失效。

- 如果作品具有交互式用户界面，则每个用户界面都必须显示适当的法律声明;但是，如果程序具有不显示适当法律声明的交互式界面，则您的工作无需显示相应的法律声明。

如果汇编及其产生的版权不用于限制汇编用户对所涵盖作品的访问或合法权利，则与其他单独和独立作品的汇编，这些作品本质上不是所涵盖作品的延伸，并且不与它结合，例如在存储或分发介质的卷内或体积上形成更大的程序，则称为“聚合”个人工程许可证。将涵盖的作品包含在聚合中不会导致本许可适用于聚合的其他部分。

6. **传达非源码形式。**

您可以根据第 4 节和第 5 节的条款以目标代码形式传达涵盖的作品，前提是您还根据本许可的条款通过以下方式之一传达机器可读的相应来源：

- 在物理产品（包括物理分发介质）中传达目标代码或体现在物理产品中，并附有固定在通常用于软件交换的耐用物理介质上的相应源。
- 在物理产品（包括物理分发介质）中传达目标代码或体现在物理产品中，并附有书面要约，有效期至少为三年，只要您为该产品型号提供备件或客户支持，就向拥有目标代码的任何人提供 （1） 本许可证涵盖的产品中所有软件的相应来源的副本， 在通常用于软件交换的耐用物理介质上，价格不超过您物理执行此源传输的合理成本，或 （2） 免费从网络服务器复制相应源。
- 将目标代码的单个副本与书面报价的副本一起传送，以提供相应的来源。此替代方案仅偶尔和非商业用途，并且仅当您收到此类要约的目标代码时，才允许根据第 6b 小节。
- 通过提供从指定位置（免费或收费）的访问来传达目标代码，并以相同的方式通过同一位置提供对相应源的等效访问，无需进一步收费。您无需要求收件人复制相应的源以及目标代码。如果复制目标代码的位置是网络服务器，则相应源可能位于支持等效复制功能的其他服务器上（由您或第三方操作），前提是您在目标代码旁边保持明确的说明，说明在哪里可以找到相应的源。无论哪个服务器托管相应的源，您都有义务确保它在满足这些要求所需的时间内可用。
- 使用点对点传输传达目标代码，前提是您告知其他对等方根据第 6d 小节免费向公众提供目标代码和作品的相应来源。

目标代码的可分离部分，其源代码作为系统库从相应的源代码中排除，不需要包含在传达目标代码工作时。

“用户产品”是 （1） “消费产品”，即通常用于个人、家庭或家庭目的的任何有形个人财产，或 （2） 为纳入住宅而设计或出售的任何物品。在确定产品是否为消费品时，应解决可疑情况，以有利于承保范围。对于特定用户收到的特定产品，“正常使用”是指该类产品的典型或常见用途，无论特定用户的状态如何，也无论特定用户实际使用或期望或预期使用产品的方式如何。产品是消费品，无论该产品是否具有实质性的商业、工业或非消费用途，除非此类用途代表该产品的唯一重要使用方式。

用户产品的“安装信息”是指从相应来源的修改版本安装和执行该用户产品中涵盖作品的修改版本所需的任何方法、程序、授权密钥或其他信息。这些信息必须足以确保修改后的目标代码的继续运行在任何情况下都不会仅仅因为进行了修改而受到阻止或干扰。

如果您在用户产品中或与用户产品一起或专门用于用户产品中，根据本节传递目标代码，并且该转让作为交易的一部分发生，其中用户产品的占有权和使用权永久或固定期限地转让给接收方（无论交易如何定性）， 本节下传达的相应来源必须附有安装信息。但是，如果您和任何第三方都不保留在用户产品上安装修改后的目标代码的能力（例如，作品已安装在ROM中），则此要求不适用。

提供安装信息的要求不包括继续为接收方修改或安装的作品或已修改或安装的用户产品提供支持服务、保修或更新的要求。当修改本身对网络的运行产生重大不利影响或违反网络通信的规则和协议时，可能会拒绝访问网络。

根据本节的规定，传达的相应来源和提供的安装信息必须采用公开记录的格式（并以源代码形式向公众提供实施），并且必须不需要特殊的密码或密钥来解压缩、读取或复制。

7 **附加条款。**

“附加权限”是通过对本许可的一个或多个条件进行例外来补充本许可条款的条款。适用于整个程序的其他许可应被视为包含在本许可中，只要它们在适用法律下有效。如果附加权限仅适用于程序的一部分，则该部分可以在这些权限下单独使用，但整个程序仍受本许可的约束，而不考虑附加权限。

当您传送所涵盖作品的副本时，您可以选择从该副本或其任何部分中删除任何其他权限。（在某些情况下，当您修改作品时，可能会编写其他权限以要求自行删除。您可以对您添加到涵盖作品中的材料授予额外的权限，您拥有或可以授予适当的版权许可。

尽管本许可有任何其他规定，对于您添加到涵盖作品中的材料，您可以（如果该材料的版权所有者授权）使用以下条款补充本许可的条款：

- 不承担与本许可第 15 节和第 16 节条款不同的保证或限制责任;或
- 要求在该材料或包含该材料的作品展示的适当法律声明中保留指定的合理法律声明或作者归属;或
- 禁止歪曲该材料的来源，或要求以不同于原始版本的合理方式标记此类材料的修改版本;或
- 限制为宣传目的使用材料的许可人或作者的姓名;或
- 拒绝根据商标法授予使用某些商品名称、商标或服务标志的权利;或
- 要求任何向接收者承担合同责任承担的材料（或其修改版本）的人对该材料的许可人和作者进行赔偿，以承担这些合同假设直接强加给这些许可人和作者的任何责任。

所有其他非许可性附加条款均被视为第 10 节意义上的“进一步限制”。如果您收到的程序或其任何部分包含声明，说明其受本许可管辖以及作为进一步限制的条款，您可以删除该条款。如果许可文档包含进一步的限制，但允许根据本许可重新许可或转让，您可以添加到受该许可文件条款约束的涵盖工作材料中，前提是进一步的限制在此类重新许可或转让后无效。

如果您根据本节向涵盖的作品添加条款，您必须在相关源文件中放置适用于这些文件的附加条款的声明，或指明在哪里可以找到适用条款的通知。

附加条款，无论是允许的还是非允许的，都可以以单独书面许可的形式说明，或作为例外情况陈述;无论哪种方式，上述要求都适用。

8. **终止。**

除非本许可明确规定，否则您不得传播或修改涵盖的作品。任何以其他方式传播或修改的尝试均无效，并将自动终止您在本许可下的权利（包括根据第 11 节第三段授予的任何专利许可）。

但是，如果您停止所有违反本许可的行为，则 （a） 暂时恢复您来自特定版权所有者的许可，除非并且直到版权所有者明确并最终终止您的许可，以及 （b） 永久恢复，如果版权所有者未能在停止后 60 天内通过某种合理方式通知您违规行为。

此外，如果版权所有者通过某种合理的方式通知您违规行为，这是您第一次收到该版权所有者（对于任何作品）违反本许可证的通知，并且您在收到通知后 30 天之前纠正了违规行为，则您来自特定版权所有者的许可将被永久恢复。

终止您在本节下的权利并不终止根据本许可从您那里获得副本或权利的各方的许可。如果您的权利已被终止且未永久恢复，则您没有资格根据第 10 节获得相同材料的新许可。

9. **拥有副本不需要接受。**

您无需接受本许可即可接收或运行程序的副本。仅由于使用点对点传输接收副本而发生的所涵盖作品的辅助传播同样不需要接受。但是，除本许可证外，您不得授予您传播或修改任何涵盖作品的权限。如果您不接受本许可，这些行为将侵犯版权。因此，修改或传播涵盖的作品，即表示您接受本许可。

10. **自动许可下游收件人。**
每次您转让涵盖的作品时，接收者都会自动收到原始许可人的许可，以运行、修改和传播该作品，但须遵守本许可。您不负责强制第三方遵守本许可。

“实体交易”是指转移一个组织的控制权或一个组织的实质上所有资产，或细分一个组织或合并组织的交易。如果所涉作品的传播来自实体交易，则收到作品副本的该交易的每一方还获得该方的前任根据上款已经或可以给予的作品的任何许可，以及拥有来自利益关系的前任作品的相应来源的权利， 如果前任拥有它或可以通过合理的努力获得它。

您不得对行使本许可授予或确认的权利施加任何进一步的限制。例如，您不得因行使本许可授予的权利而征收许可费、版税或其他费用，并且您不得提起诉讼（包括诉讼中的交叉索赔或反索赔），声称通过制造、使用、销售、提供销售或进口程序或其任何部分侵犯了任何专利索赔。

11. **专利。**

“贡献者”是根据本许可证授权使用程序或程序所基于的作品的版权所有者。这样获得许可的作品被称为贡献者的“贡献者版本”。

贡献者的“基本专利权利要求”是指贡献者拥有或控制的所有专利权利要求，无论是已经获得的还是以后获得的，这些权利要求将以某种方式被本许可证允许的制作、使用或销售其贡献者版本所侵犯，但不包括仅因进一步修改贡献者版本而侵权的权利要求。就本定义而言，“控制”包括以符合本许可要求的方式授予专利分许可的权利。

每个贡献者根据贡献者的基本专利声明授予您非排他性的、全球性的、免版税的专利许可，以制作、使用、出售、要约出售、导入和以其他方式运行、修改和传播其贡献者版本的内容。

在以下三段中，“专利许可”是指不执行专利的任何明确协议或承诺，无论其名称如何（例如明确允许实施专利或不起诉专利侵权）。向一方“授予”此类专利许可意味着达成此类协议或承诺不对该方执行专利。

如果您故意依赖专利许可转让涵盖的作品，并且根据本许可的条款，任何人都无法通过公开可用的网络服务器或其他易于访问的方式免费复制该作品的相应来源，那么您必须 （1） 使相应来源如此可用， 或 （2） 安排剥夺您自己对该特定作品的专利许可的好处，或 （3） 安排以符合本许可要求的方式将专利许可扩展到下游接收者。“故意依赖”意味着您实际知道，如果没有专利许可，您在某个国家/地区转让所涵盖的作品，或您的接收者在某个国家/地区使用所涵盖的作品，将侵犯该国家/地区的一项或多项您有理由相信有效的可识别专利。

如果您根据或与单一交易或安排有关，通过购买涵盖作品的转让来转让或传播，并向接收涵盖作品的某些方授予专利许可，授权他们使用、传播、修改或转让涵盖作品的特定副本，则您授予的专利许可将自动扩展到涵盖作品和基于该作品的作品的所有接收者。

如果专利许可不包括在其涵盖范围内，禁止行使或以不行使本许可明确授予的一项或多项权利为条件，则该专利许可是“歧视性的”。如果您是与从事软件分发业务的第三方达成的安排的一方，您不得转让涵盖的作品，根据该安排，您根据该安排根据您转让作品的活动范围向第三方付款，并且第三方授予将从您那里收到涵盖作品的任何一方， 歧视性专利许可 （a） 与您传送的涵盖作品的副本（或由这些副本制作的副本）有关，或 （b） 主要针对包含涵盖作品的特定产品或汇编，除非您在 2007 年 3 月 28 日之前签订了该安排或授予了该专利许可。

本许可中的任何内容均不得解释为排除或限制根据适用的专利法您可能获得的任何默示许可或其他侵权抗辩。

12. **不放弃他人的自由。**

如果对您施加的条件（无论是通过法院命令、协议还是其他方式）与本许可证的条件相抵触，则它们不会免除您遵守本许可证的条件。如果您无法同时履行您在本许可下的义务和任何其他相关义务而转让涵盖的作品，那么因此您可能根本不会转让该作品。例如，如果您同意有义务向您转让程序的人收取版税以进一步转让的条款，则您同时满足这些条款和本许可的唯一方法是完全避免转让本程序。

13. **与 GNU Affero 通用公共许可证一起使用。**

尽管本许可证有任何其他规定，您仍有权将任何涵盖的作品与根据 GNU Affero 通用公共许可证版本 3 许可的作品链接或合并为单个组合作品，并传达由此产生的作品。本许可证的条款将继续适用于所涵盖作品的部分，但 GNU Affero 通用公共许可证第 13 节中关于通过网络进行交互的特殊要求将适用于此类组合。

14. **本许可证的修订版本。**

自由软件基金会可能会不时发布 GNU 通用公共许可证的修订版和/或新版本。这些新版本在精神上与现有版本相似，但在细节上可能有所不同，以解决新的问题或关切。

每个版本都有一个可区分的版本号。如果程序指定 GNU 通用公共许可证的某个编号版本“或任何更高版本”适用于它，您可以选择遵循该编号版本或自由软件基金会发布的任何更高版本的条款和条件。如果程序没有指定 GNU 通用公共许可证的版本号，您可以选择自由软件基金会发布的任何版本。

如果程序指定代理可以决定可以使用哪些未来版本的 GNU 通用公共许可证，则该代理接受某个版本的公开声明将永久授权您为程序选择该版本。

更高版本的许可证可能会为您提供其他或不同的权限。但是，不会因您选择遵循更高版本而对任何作者或版权所有者施加额外的义务。

15. **免责声明。**

在适用法律允许的范围内，本计划不提供任何保证。除非另有书面说明，否则版权所有者和/或其他方“按原样”提供本程序，不提供任何明示或暗示的保证，包括但不限于对适销性和特定用途适用性的暗示保证。有关程序质量和性能的全部风险由您承担。如果程序证明有缺陷，您将承担所有必要的服务、维修或纠正费用。

16. **责任限制。**

在任何情况下，除非适用法律要求或书面同意，否则任何版权所有者或根据上述允许修改和/或传达程序的任何其他方均不对您承担损害赔偿责任，包括因使用或无法使用程序而引起的任何一般、特殊、偶然或后果性损害（包括但不限于数据丢失或数据变得不准确或您遭受的损失或遭受的损失或第三方或程序未能与任何其他程序一起运行），即使此类持有人或其他方已被告知此类损害的可能性。

17. **对第15条和第16条的解释。**

如果上述免责声明和责任限制无法根据其条款赋予当地法律效力，则审查法院应适用最接近与计划相关的所有民事责任的绝对放弃的当地法律，除非保证或责任承担附带程序副本以换取费用。

**条款和条件结束**
# 如何将这些条款应用于您的新计划
如果你开发了一个新的程序，并且你希望它对公众有最大的用处，那么实现这一目标的最好方法是使其成为自由软件，每个人都可以根据这些条款重新分发和更改。

为此，请将以下通知附加到程序中。最安全的做法是将它们附加到每个源文件的开头，以最有效地说明保修的排除;每个文件至少应具有“版权”行和指向找到完整通知的位置的指针。
```
one line to give the program's name and a brief idea of what it does.
Copyright (C) year name of author

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
```
另添加有关如何通过电子邮件和纸质邮件与您联系的信息。

如果程序进行终端交互，则在以交互模式启动时使其输出如下简短通知：
```
program Copyright (C) year name of author
This program comes with ABSOLUTELY NO WARRANTY; for details type ‘show w’.
This is free software, and you are welcome to redistribute it
under certain conditions; type ‘show c’ for details.
```
假设的命令“”和“”应显示通用公共许可证的相应部分。当然，程序的命令可能不同;对于 GUI 界面，您将使用“关于框”。show wshow c

如有必要，您还应该让您的雇主（如果您是程序员）或学校（如果有的话）签署该程序的“版权免责声明”。有关这方面的更多信息，以及如何应用和遵循 GNU GPL，请参阅 https://www.gnu.org/licenses/。

GNU 通用公共许可证不允许将您的程序合并到专有程序中。如果您的程序是一个子例程库，您可能会认为允许将专有应用程序与库链接更有用。如果这是您想要做的，请使用 GNU 宽通用公共许可证而不是本许可证。但首先，请阅读 https://www.gnu.org/licenses/why-not-lgpl.html。

# 3 Bison Grammar Files
Bison takes as input a context-free grammar specification and produces a C-language function that recognizes correct instances of the grammar.

The Bison grammar file conventionally has a name ending in ‘.y’. 
## 3.1 Outline of a Bison Grammar
A Bison grammar file has four main sections, shown here with the appropriate delimiters:
```c
%{
  Prologue
%}

Bison declarations

%%
Grammar rules
%%

Epilogue
```
Comments enclosed in ‘/* … */’ may appear in any of the sections. As a GNU extension, ‘//’ introduces a comment that continues until end of line.

### 3.1.1 The prologue
The Prologue section contains macro definitions and declarations of functions and variables that are used in the actions in the grammar rules. These are copied to the beginning of the parser implementation file so that they precede the definition of yyparse. You can use ‘#include’ to get the declarations from a header file. If you don’t need any C declarations, you may omit the ‘%{’ and ‘%}’ delimiters that bracket this section.

The Prologue section is terminated by the first occurrence of ‘%}’ that is outside a comment, a string literal, or a character constant.

You may have more than one Prologue section, intermixed with the Bison declarations. This allows you to have C and Bison declarations that refer to each other. For example, the %union declaration may use types defined in a header file, and you may wish to prototype functions that take arguments of type YYSTYPE. This can be done with two Prologue blocks, one before and one after the %union declaration.
```c
%{
  #define _GNU_SOURCE
  #include <stdio.h>
  #include "ptypes.h"
%}

%union {
  long n;
  tree t;  /* tree is defined in ptypes.h. */
}

%{
  static void print_token (yytoken_kind_t token, YYSTYPE val);
%}

…
```
When in doubt, it is usually safer to put prologue code before all Bison declarations, rather than after. For example, any definitions of feature test macros like _GNU_SOURCE or _POSIX_C_SOURCE should appear before all Bison declarations, as feature test macros can affect the behavior of Bison-generated #include directives.

### 3.1.2 Prologue Alternatives
The functionality of Prologue sections can often be subtle and inflexible. As an alternative, Bison provides a %code directive with an explicit qualifier field, which identifies the purpose of the code and thus the location(s) where Bison should generate it. For C/C++, the qualifier can be omitted for the default location, or it can be one of requires, provides, top. See %code Summary.

Look again at the example of the previous section:
```c
%{
  #define _GNU_SOURCE
  #include <stdio.h>
  #include "ptypes.h"
%}

%union {
  long n;
  tree t;  /* tree is defined in ptypes.h. */
}

%{
  static void print_token (yytoken_kind_t token, YYSTYPE val);
%}

…
```
Notice that there are two Prologue sections here, but there’s a subtle distinction between their functionality. For example, if you decide to override Bison’s default definition for YYLTYPE, in which Prologue section should you write your new definition? You should write it in the first since Bison will insert that code into the parser implementation file before the default YYLTYPE definition. In which Prologue section should you prototype an internal function, trace_token, that accepts YYLTYPE and yytoken_kind_t as arguments? You should prototype it in the second since Bison will insert that code after the YYLTYPE and yytoken_kind_t definitions.

This distinction in functionality between the two Prologue sections is established by the appearance of the %union between them. This behavior raises a few questions. First, why should the position of a %union affect definitions related to YYLTYPE and yytoken_kind_t? Second, what if there is no %union? In that case, the second kind of Prologue section is not available. This behavior is not intuitive.

To avoid this subtle %union dependency, rewrite the example using a %code top and an unqualified %code. Let’s go ahead and add the new YYLTYPE definition and the trace_token prototype at the same time:
```c
%code top {
  #define _GNU_SOURCE
  #include <stdio.h>

  /* WARNING: The following code really belongs
   * in a '%code requires'; see below. */

  #include "ptypes.h"
  #define YYLTYPE YYLTYPE
  typedef struct YYLTYPE
  {
    int first_line;
    int first_column;
    int last_line;
    int last_column;
    char *filename;
  } YYLTYPE;
}

%union {
  long n;
  tree t;  /* tree is defined in ptypes.h. */
}

%code {
  static void print_token (yytoken_kind_t token, YYSTYPE val);
  static void trace_token (yytoken_kind_t token, YYLTYPE loc);
}

…
```
In this way, %code top and the unqualified %code achieve the same functionality as the two kinds of Prologue sections, but it’s always explicit which kind you intend. Moreover, both kinds are always available even in the absence of %union.

The %code top block above logically contains two parts. The first two lines before the warning need to appear near the top of the parser implementation file. The first line after the warning is required by YYSTYPE and thus also needs to appear in the parser implementation file. However, if you’ve instructed Bison to generate a parser header file (see Bison Declaration Summary), you probably want that line to appear before the YYSTYPE definition in that header file as well. The YYLTYPE definition should also appear in the parser header file to override the default YYLTYPE definition there.

In other words, in the %code top block above, all but the first two lines are dependency code required by the YYSTYPE and YYLTYPE definitions. Thus, they belong in one or more %code requires:
```c
%code top {
  #define _GNU_SOURCE
  #include <stdio.h>
}

%code requires {
  #include "ptypes.h"
}
%union {
  long n;
  tree t;  /* tree is defined in ptypes.h. */
}

%code requires {
  #define YYLTYPE YYLTYPE
  typedef struct YYLTYPE
  {
    int first_line;
    int first_column;
    int last_line;
    int last_column;
    char *filename;
  } YYLTYPE;
}

%code {
  static void print_token (yytoken_kind_t token, YYSTYPE val);
  static void trace_token (yytoken_kind_t token, YYLTYPE loc);
}

…
```
Now Bison will insert #include "ptypes.h" and the new YYLTYPE definition before the Bison-generated YYSTYPE and YYLTYPE definitions in both the parser implementation file and the parser header file. (By the same reasoning, %code requires would also be the appropriate place to write your own definition for YYSTYPE.)

When you are writing dependency code for YYSTYPE and YYLTYPE, you should prefer %code requires over %code top regardless of whether you instruct Bison to generate a parser header file. When you are writing code that you need Bison to insert only into the parser implementation file and that has no special need to appear at the top of that file, you should prefer the unqualified %code over %code top. These practices will make the purpose of each block of your code explicit to Bison and to other developers reading your grammar file. Following these practices, we expect the unqualified %code and %code requires to be the most important of the four Prologue alternatives.

At some point while developing your parser, you might decide to provide trace_token to modules that are external to your parser. Thus, you might wish for Bison to insert the prototype into both the parser header file and the parser implementation file. Since this function is not a dependency required by YYSTYPE or YYLTYPE, it doesn’t make sense to move its prototype to a %code requires. More importantly, since it depends upon YYLTYPE and yytoken_kind_t, %code requires is not sufficient. Instead, move its prototype from the unqualified %code to a %code provides:
```c
%code top {
  #define _GNU_SOURCE
  #include <stdio.h>
}

%code requires {
  #include "ptypes.h"
}
%union {
  long n;
  tree t;  /* tree is defined in ptypes.h. */
}

%code requires {
  #define YYLTYPE YYLTYPE
  typedef struct YYLTYPE
  {
    int first_line;
    int first_column;
    int last_line;
    int last_column;
    char *filename;
  } YYLTYPE;
}

%code provides {
  void trace_token (yytoken_kind_t token, YYLTYPE loc);
}

%code {
  static void print_token (FILE *file, int token, YYSTYPE val);
}

…
```
Bison will insert the trace_token prototype into both the parser header file and the parser implementation file after the definitions for yytoken_kind_t, YYLTYPE, and YYSTYPE.

The above examples are careful to write directives in an order that reflects the layout of the generated parser implementation and header files: %code top, %code requires, %code provides, and then %code. While your grammar files may generally be easier to read if you also follow this order, Bison does not require it. Instead, Bison lets you choose an organization that makes sense to you.

You may declare any of these directives multiple times in the grammar file. In that case, Bison concatenates the contained code in declaration order. This is the only way in which the position of one of these directives within the grammar file affects its functionality.

The result of the previous two properties is greater flexibility in how you may organize your grammar file. For example, you may organize semantic-type-related directives by semantic type:
```c
%code requires { #include "type1.h" }
%union { type1 field1; }
%destructor { type1_free ($$); } <field1>
%printer { type1_print (yyo, $$); } <field1>

%code requires { #include "type2.h" }
%union { type2 field2; }
%destructor { type2_free ($$); } <field2>
%printer { type2_print (yyo, $$); } <field2>
```
You could even place each of the above directive groups in the rules section of the grammar file next to the set of rules that uses the associated semantic type. (In the rules section, you must terminate each of those directives with a semicolon.) And you don’t have to worry that some directive (like a %union) in the definitions section is going to adversely affect their functionality in some counter-intuitive manner just because it comes first. Such an organization is not possible using Prologue sections.

This section has been concerned with explaining the advantages of the four Prologue alternatives over the original Yacc Prologue. However, in most cases when using these directives, you shouldn’t need to think about all the low-level ordering issues discussed here. Instead, you should simply use these directives to label each block of your code according to its purpose and let Bison handle the ordering. %code is the most generic label. Move code to %code requires, %code provides, or %code top as needed.

### 3.1.3 The Bison Declarations Section
The Bison declarations section contains declarations that define terminal and nonterminal symbols, specify precedence, and so on. In some simple grammars you may not need any declarations.

### 3.1.4 The Grammar Rules Section
The grammar rules section contains one or more Bison grammar rules, and nothing else. 

There must always be at least one grammar rule, and the first ‘%%’ (which precedes the grammar rules) may never be omitted even if it is the first thing in the file.

### 3.1.5 The epilogue
The Epilogue is copied verbatim to the end of the parser implementation file, just as the Prologue is copied to the beginning. This is the most convenient place to put anything that you want to have in the parser implementation file but which need not come before the definition of yyparse. For example, the definitions of yylex and yyerror often go here. Because C requires functions to be declared before being used, you often need to declare functions like yylex and yyerror in the Prologue, even if you define them in the Epilogue. See Parser C-Language Interface.

If the last section is empty, you may omit the ‘%%’ that separates it from the grammar rules.

The Bison parser itself contains many macros and identifiers whose names start with ‘yy’ or ‘YY’, so it is a good idea to avoid using any such names (except those documented in this manual) in the epilogue of the grammar file.

## 3.2 Symbols, Terminal and Nonterminal
Symbols in Bison grammars represent the grammatical classifications of the language.

A terminal symbol (also known as a token kind) represents a class of syntactically equivalent tokens. You use the symbol in grammar rules to mean that a token in that class is allowed. The symbol is represented in the Bison parser by a numeric code, and the yylex function returns a token kind code to indicate what kind of token has been read. You don’t need to know what the code value is; you can use the symbol to stand for it.

A nonterminal symbol stands for a class of syntactically equivalent groupings. The symbol name is used in writing grammar rules. By convention, it should be all lower case.

Symbol names can contain letters, underscores, periods, and non-initial digits and dashes. Dashes in symbol names are a GNU extension, incompatible with POSIX Yacc. Periods and dashes make symbol names less convenient to use with named references, which require brackets around such names (see Named References). Terminal symbols that contain periods or dashes make little sense: since they are not valid symbols (in most programming languages) they are not exported as token names.

There are three ways of writing terminal symbols in the grammar:

- A named token kind is written with an identifier, like an identifier in C. By convention, it should be all upper case. Each such name must be defined with a Bison declaration such as %token. See Token Kind Names.
A character token kind (or literal character token) is written in the grammar using the same syntax used in C for character constants; for example, '+' is a character token kind. A character token kind doesn’t need to be declared unless you need to specify its semantic value data type (see Data Types of Semantic Values), associativity, or precedence (see Operator Precedence).  
By convention, a character token kind is used only to represent a token that consists of that particular character. Thus, the token kind '+' is used to represent the character ‘+’ as a token. Nothing enforces this convention, but if you depart from it, your program will confuse other readers.

- All the usual escape sequences used in character literals in C can be used in Bison as well, but you must not use the null character as a character literal because its numeric code, zero, signifies end-of-input (see Calling Convention for yylex). Also, unlike standard C, trigraphs have no special meaning in Bison character literals, nor is backslash-newline allowed.

- A literal string token is written like a C string constant; for example, "<=" is a literal string token. A literal string token doesn’t need to be declared unless you need to specify its semantic value data type (see Data Types of Semantic Values), associativity, or precedence (see Operator Precedence).  
You can associate the literal string token with a symbolic name as an alias, using the %token declaration (see Token Kind Names). If you don’t do that, the lexical analyzer has to retrieve the token code for the literal string token from the yytname table (see Calling Convention for yylex).  
**Warning**: literal string tokens do not work in Yacc.  
By convention, a literal string token is used only to represent a token that consists of that particular string. Thus, you should use the token kind "<=" to represent the string ‘<=’ as a token. Bison does not enforce this convention, but if you depart from it, people who read your program will be confused.  
All the escape sequences used in string literals in C can be used in Bison as well, except that you must not use a null character within a string literal. Also, unlike Standard C, trigraphs have no special meaning in Bison string literals, nor is backslash-newline allowed. A literal string token must contain two or more characters; for a token containing just one character, use a character token (see above).

How you choose to write a terminal symbol has no effect on its grammatical meaning. That depends only on where it appears in rules and on when the parser function returns that symbol.

The value returned by yylex is always one of the terminal symbols, except that a zero or negative value signifies end-of-input. Whichever way you write the token kind in the grammar rules, you write it the same way in the definition of yylex. The numeric code for a character token kind is simply the positive numeric code of the character, so yylex can use the identical value to generate the requisite code, though you may need to convert it to unsigned char to avoid sign-extension on hosts where char is signed. Each named token kind becomes a C macro in the parser implementation file, so yylex can use the name to stand for the code. (This is why periods don’t make sense in terminal symbols.) See Calling Convention for yylex.

If yylex is defined in a separate file, you need to arrange for the token-kind definitions to be available there. Use the -d option when you run Bison, so that it will write these definitions into a separate header file name.tab.h which you can include in the other source files that need it. See Invoking Bison.

If you want to write a grammar that is portable to any Standard C host, you must use only nonnull character tokens taken from the basic execution character set of Standard C. This set consists of the ten digits, the 52 lower- and upper-case English letters, and the characters in the following C-language string:
```
"\a\b\t\n\v\f\r !\"#%&'()*+,-./:;<=>?[\\]^_{|}~"
```
The yylex function and Bison must use a consistent character set and encoding for character tokens. For example, if you run Bison in an ASCII environment, but then compile and run the resulting program in an environment that uses an incompatible character set like EBCDIC, the resulting program may not work because the tables generated by Bison will assume ASCII numeric values for character tokens. It is standard practice for software distributions to contain C source files that were generated by Bison in an ASCII environment, so installers on platforms that are incompatible with ASCII must rebuild those files before compiling them.

The symbol error is a terminal symbol reserved for error recovery (see Error Recovery); you shouldn’t use it for any other purpose. In particular, yylex should never return this value. The default value of the error token is 256, unless you explicitly assigned 256 to one of your tokens with a %token declaration.

## 3.3 Grammar Rules
A Bison grammar is a list of rules.
### 3.3.1 Syntax of Grammar Rules
A Bison grammar rule has the following general form:
```c
result: components…;
```
where result is the nonterminal symbol that this rule describes, and components are various terminal and nonterminal symbols that are put together by this rule (see Symbols, Terminal and Nonterminal).

For example,
```c
exp: exp '+' exp;
```
says that two groupings of type exp, with a ‘+’ token in between, can be combined into a larger grouping of type exp.

White space in rules is significant only to separate symbols. You can add extra white space as you wish.

Scattered among the components can be actions that determine the semantics of the rule. An action looks like this:
```c
{C statements}
```
This is an example of braced code, that is, C code surrounded by braces, much like a compound statement in C. Braced code can contain any sequence of C tokens, so long as its braces are balanced. Bison does not check the braced code for correctness directly; it merely copies the code to the parser implementation file, where the C compiler can check it.

Within braced code, the balanced-brace count is not affected by braces within comments, string literals, or character constants, but it is affected by the C digraphs ‘<%’ and ‘%>’ that represent braces. At the top level braced code must be terminated by ‘}’ and not by a digraph. Bison does not look for trigraphs, so if braced code uses trigraphs you should ensure that they do not affect the nesting of braces or the boundaries of comments, string literals, or character constants.

Usually there is only one action and it follows the components. 

Multiple rules for the same result can be written separately or can be joined with the vertical-bar character ‘|’ as follows:
```c
result:
  rule1-components…
| rule2-components…
…
;
```
They are still considered distinct rules even when joined in this way.

### 3.3.2 Empty Rules
A rule is said to be empty if its right-hand side (components) is empty. It means that result in the previous example can match the empty string. As another example, here is how to define an optional semicolon:
```c
semicolon.opt: | ";";
```
It is easy not to see an empty rule, especially when | is used. The %empty directive allows to make explicit that a rule is empty on purpose:
```c
semicolon.opt:
  %empty
| ";"
;
```
Flagging a non-empty rule with %empty is an error. If run with -Wempty-rule, bison will report empty rules without %empty. Using %empty enables this warning, unless -Wno-empty-rule was specified.

The %empty directive is a Bison extension, it does not work with Yacc. To remain compatible with POSIX Yacc, it is customary to write a comment ‘/* empty */’ in each rule with no components:
```c
semicolon.opt:
  /* empty */
| ";"
;
```

### 3.3.3 Recursive Rules
A rule is called recursive when its result nonterminal appears also on its right hand side. Nearly all Bison grammars need to use recursion, because that is the only way to define a sequence of any number of a particular thing. Consider this recursive definition of a comma-separated sequence of one or more expressions:
```c
expseq1:
  exp
| expseq1 ',' exp
;
```
Since the recursive use of expseq1 is the leftmost symbol in the right hand side, we call this left recursion. By contrast, here the same construct is defined using right recursion:
```c
expseq1:
  exp
| exp ',' expseq1
;
```
Any kind of sequence can be defined using either left recursion or right recursion, but you should always use left recursion, because it can parse a sequence of any number of elements with bounded stack space. Right recursion uses up space on the Bison stack in proportion to the number of elements in the sequence, because all the elements must be shifted onto the stack before the rule can be applied even once. See The Bison Parser Algorithm, for further explanation of this.

Indirect or mutual recursion occurs when the result of the rule does not appear directly on its right hand side, but does appear in rules for other nonterminals which do appear on its right hand side.

For example:
```
expr:
  primary
| primary '+' primary
;

primary:
  constant
| '(' expr ')'
;
```
defines two mutually-recursive nonterminals, since each refers to the other.

## 3.4 Defining Language Semantics
The grammar rules for a language determine only the syntax. The semantics are determined by the semantic values associated with various tokens and groupings, and by the actions taken when various groupings are recognized.

For example, the calculator calculates properly because the value associated with each expression is the proper number; it adds properly because the action for the grouping ‘x + y’ is to add the numbers associated with x and y.

### 3.4.1 Data Types of Semantic Values
In a simple program it may be sufficient to use the same data type for the semantic values of all language constructs. This was true in the RPN and infix calculator examples (see Reverse Polish Notation Calculator).

Bison normally uses the type int for semantic values if your program uses the same data type for all language constructs. To specify some other type, define the %define variable api.value.type like this:
```c
%define api.value.type {double}
```
or
```c
%define api.value.type {struct semantic_value_type}
```
The value of api.value.type should be a type name that does not contain parentheses or square brackets.

Alternatively in C, instead of relying of Bison’s %define support, you may rely on the C preprocessor and define YYSTYPE as a macro:
```c
#define YYSTYPE double
```
This macro definition must go in the prologue of the grammar file (see Outline of a Bison Grammar). If compatibility with POSIX Yacc matters to you, use this. Note however that Bison cannot know YYSTYPE’s value, not even whether it is defined, so there are services it cannot provide. Besides this works only for C.

### 3.4.2 More Than One Value Type
In most programs, you will need different data types for different kinds of tokens and groupings. For example, a numeric constant may need type int or long, while a string constant needs type char *, and an identifier might need a pointer to an entry in the symbol table.

To use more than one data type for semantic values in one parser, Bison requires you to do two things:

- Specify the entire collection of possible data types. There are several options:
1. let Bison compute the union type from the tags you assign to symbols;
2. use the %union Bison declaration (see The Union Declaration);
3. define the %define variable api.value.type to be a union type whose members are the type tags (see Providing a Structured Semantic Value Type);
4. use a typedef or a #define to define YYSTYPE to be a union type whose member names are the type tags.
- Choose one of those types for each symbol (terminal or nonterminal) for which semantic values are used. This is done for tokens with the %token Bison declaration (see Token Kind Names) and for groupings with the %nterm/%type Bison declarations (see Nonterminal Symbols).

### 3.4.3 Generating the Semantic Value Type
The special value union of the %define variable api.value.type instructs Bison that the type tags (used with the %token, %nterm and %type directives) are genuine types, not names of members of YYSTYPE.

For example:
```c
%define api.value.type union
%token <int> INT "integer"
%token <int> 'n'
%nterm <int> expr
%token <char const *> ID "identifier"
```
generates an appropriate value of YYSTYPE to support each symbol type. The name of the member of YYSTYPE for tokens than have a declared identifier id (such as INT and ID above, but not 'n') is id. The other symbols have unspecified names on which you should not depend; instead, relying on C casts to access the semantic value with the appropriate type:
```c
/* For an "integer". */
yylval.INT = 42;
return INT;

/* For an 'n', also declared as int. */
*((int*)&yylval) = 42;
return 'n';

/* For an "identifier". */
yylval.ID = "42";
return ID;
```
If the %define variable api.token.prefix is defined (see %define Summary), then it is also used to prefix the union member names. For instance, with ‘%define api.token.prefix {TOK_}’:
```
/* For an "integer". */
yylval.TOK_INT = 42;
return TOK_INT;
```
This Bison extension cannot work if %yacc (or -y/--yacc) is enabled, as POSIX mandates that Yacc generate tokens as macros (e.g., ‘#define INT 258’, or ‘#define TOK_INT 258’).

A similar feature is provided for C++ that in addition overcomes C++ limitations (that forbid non-trivial objects to be part of a union): ‘%define api.value.type variant’, see C++ Variants.\

### 3.4.4 The Union Declaration
The %union declaration specifies the entire collection of possible data types for semantic values. The keyword %union is followed by braced code containing the same thing that goes inside a union in C.

For example:
```c
%union {
  double val;
  symrec *tptr;
}
```
This says that the two alternative types are double and symrec *. They are given names val and tptr; these names are used in the %token, %nterm and %type declarations to pick one of the types for a terminal or nonterminal symbol (see Nonterminal Symbols).

As an extension to POSIX, a tag is allowed after the %union. For example:
```c
%union value {
  double val;
  symrec *tptr;
}
```
specifies the union tag value, so the corresponding C type is union value. If you do not specify a tag, it defaults to YYSTYPE (see %define Summary).

As another extension to POSIX, you may specify multiple %union declarations; their contents are concatenated. However, only the first %union declaration can specify a tag.

Note that, unlike making a union declaration in C, you need not write a semicolon after the closing brace.

### 3.4.5 Providing a Structured Semantic Value Type
Instead of %union, you can define and use your own union type YYSTYPE if your grammar contains at least one ‘<type>’ tag. For example, you can put the following into a header file parser.h:
```c
union YYSTYPE {
  double val;
  symrec *tptr;
};
```
and then your grammar can use the following instead of %union:
```c
%{
#include "parser.h"
%}
%define api.value.type {union YYSTYPE}
%nterm <val> expr
%token <tptr> ID
```
Actually, you may also provide a struct rather that a union, which may be handy if you want to track information for every symbol (such as preceding comments).

The type you provide may even be structured and include pointers, in which case the type tags you provide may be composite, with ‘.’ and ‘->’ operators.

### 3.4.6 Actions
An action accompanies a syntactic rule and contains C code to be executed each time an instance of that rule is recognized. The task of most actions is to compute a semantic value for the grouping built by the rule from the semantic values associated with tokens or smaller groupings.

An action consists of braced code containing C statements, and can be placed at any position in the rule; it is executed at that position. Most rules have just one action at the end of the rule, following all the components. Actions in the middle of a rule are tricky and used only for special purposes (see Actions in Midrule).

The C code in an action can refer to the semantic values of the components matched by the rule with the construct $n, which stands for the value of the nth component. The semantic value for the grouping being constructed is $$. In addition, the semantic values of symbols can be accessed with the named references construct $name or $[name]. Bison translates both of these constructs into expressions of the appropriate type when it copies the actions into the parser implementation file. $$ (or $name, when it stands for the current grouping) is translated to a modifiable lvalue, so it can be assigned to.

Here is a typical example:
```c
exp:
…
| exp '+' exp     { $$ = $1 + $3; }
```
Or, in terms of named references:
```c
exp[result]:
…
| exp[left] '+' exp[right]  { $result = $left + $right; }
```
This rule constructs an exp from two smaller exp groupings connected by a plus-sign token. In the action, $1 and $3 ($left and $right) refer to the semantic values of the two component exp groupings, which are the first and third symbols on the right hand side of the rule. The sum is stored into $$ ($result) so that it becomes the semantic value of the addition-expression just recognized by the rule. If there were a useful semantic value associated with the ‘+’ token, it could be referred to as $2.

See Named References, for more information about using the named references construct.

Note that the vertical-bar character ‘|’ is really a rule separator, and actions are attached to a single rule. This is a difference with tools like Flex, for which ‘|’ stands for either “or”, or “the same action as that of the next rule”. In the following example, the action is triggered only when ‘b’ is found:
```c
a-or-b: 'a'|'b'   { a_or_b_found = 1; };
```
If you don’t specify an action for a rule, Bison supplies a default: $$ = $1. Thus, the value of the first symbol in the rule becomes the value of the whole rule. Of course, the default action is valid only if the two data types match. There is no meaningful default action for an empty rule; every empty rule must have an explicit action unless the rule’s value does not matter.

$n with n zero or negative is allowed for reference to tokens and groupings on the stack before those that match the current rule. This is a very risky practice, and to use it reliably you must be certain of the context in which the rule is applied. Here is a case in which you can use this reliably:
```c
foo:
  expr bar '+' expr  { … }
| expr bar '-' expr  { … }
;

bar:
  %empty    { previous_expr = $0; }
;
```
As long as bar is used only in the fashion shown here, $0 always refers to the expr which precedes bar in the definition of foo.

It is also possible to access the semantic value of the lookahead token, if any, from a semantic action. This semantic value is stored in yylval. See Special Features for Use in Actions.

### 3.4.7 Data Types of Values in Actions
If you have chosen a single data type for semantic values, the $$ and $n constructs always have that data type.

If you have used %union to specify a variety of data types, then you must declare a choice among these types for each terminal or nonterminal symbol that can have a semantic value. Then each time you use $$ or $n, its data type is determined by which symbol it refers to in the rule. In this example,
```c
exp:
  …
| exp '+' exp    { $$ = $1 + $3; }
```
$1 and $3 refer to instances of exp, so they all have the data type declared for the nonterminal symbol exp. If $2 were used, it would have the data type declared for the terminal symbol '+', whatever that might be.

Alternatively, you can specify the data type when you refer to the value, by inserting ‘<type>’ after the ‘$’ at the beginning of the reference. For example, if you have defined types as shown here:
```c
%union {
  int itype;
  double dtype;
}
```
then you can write $<itype>1 to refer to the first subunit of the rule as an integer, or $<dtype>1 to refer to it as a double.

### 3.4.8 Actions in Midrule
Occasionally it is useful to put an action in the middle of a rule. These actions are written just like usual end-of-rule actions, but they are executed before the parser even recognizes the following components.

#### 3.4.8.1 Using Midrule Actions
A midrule action may refer to the components preceding it using $n, but it may not refer to subsequent components because it is run before they are parsed.

The midrule action itself counts as one of the components of the rule. This makes a difference when there is another action later in the same rule (and usually there is another at the end): you have to count the actions along with the symbols when working out which number n to use in $n.

The midrule action can also have a semantic value. The action can set its value with an assignment to $$, and actions later in the rule can refer to the value using $n. Since there is no symbol to name the action, there is no way to declare a data type for the value in advance, so you must use the ‘$<…>n’ construct to specify a data type each time you refer to this value.

There is no way to set the value of the entire rule with a midrule action, because assignments to $$ do not have that effect. The only way to set the value for the entire rule is with an ordinary action at the end of the rule.

Here is an example from a hypothetical compiler, handling a let statement that looks like ‘let (variable) statement’ and serves to create a variable named variable temporarily for the duration of statement. To parse this construct, we must put variable into the symbol table while statement is parsed, then remove it afterward. Here is how it is done:
```c
stmt:
  "let" '(' var ')'
    {
      $<context>$ = push_context ();
      declare_variable ($3);
    }
  stmt
    {
      $$ = $6;
      pop_context ($<context>5);
    }
```
As soon as ‘let (variable)’ has been recognized, the first action is run. It saves a copy of the current semantic context (the list of accessible variables) as its semantic value, using alternative context in the data-type union. Then it calls declare_variable to add the new variable to that list. Once the first action is finished, the embedded statement stmt can be parsed.

Note that the midrule action is component number 5, so the ‘stmt’ is component number 6. Named references can be used to improve the readability and maintainability (see Named References):
```c
stmt:
  "let" '(' var ')'
    {
      $<context>let = push_context ();
      declare_variable ($3);
    }[let]
  stmt
    {
      $$ = $6;
      pop_context ($<context>let);
    }
```
After the embedded statement is parsed, its semantic value becomes the value of the entire let-statement. Then the semantic value from the earlier action is used to restore the prior list of variables. This removes the temporary let-variable from the list so that it won’t appear to exist while the rest of the program is parsed.

Because the types of the semantic values of midrule actions are unknown to Bison, type-based features (e.g., ‘%printer’, ‘%destructor’) do not work, which could result in memory leaks. They also forbid the use of the variant implementation of the api.value.type in C++ (see C++ Variants).

See Typed Midrule Actions, for one way to address this issue, and Midrule Action Translation, for another: turning mid-action actions into regular actions.

#### Typed Midrule Actions
In the above example, if the parser initiates error recovery (see Error Recovery) while parsing the tokens in the embedded statement stmt, it might discard the previous semantic context $<context>5 without restoring it. Thus, $<context>5 needs a destructor (see Freeing Discarded Symbols), and Bison needs the type of the semantic value (context) to select the right destructor.

As an extension to Yacc’s midrule actions, Bison offers a means to type their semantic value: specify its type tag (‘<...>’ before the midrule action.

Consider the previous example, with an untyped midrule action:
```c
stmt:
  "let" '(' var ')'
    {
      $<context>$ = push_context (); // ***
      declare_variable ($3);
    }
  stmt
    {
      $$ = $6;
      pop_context ($<context>5);     // ***
    }
```
If instead you write:
```c
stmt:
  "let" '(' var ')'
    <context>{                       // ***
      $$ = push_context ();          // ***
      declare_variable ($3);
    }
  stmt
    {
      $$ = $6;
      pop_context ($5);              // ***
    }
```
then %printer and %destructor work properly (no more leaks!), C++ variants can be used, and redundancy is reduced (<context> is specified once).

#### 3.4.8.3 Midrule Action Translation
Midrule actions are actually transformed into regular rules and actions. The various reports generated by Bison (textual, graphical, etc., see Understanding Your Parser) reveal this translation, best explained by means of an example. The following rule:
```c
exp: { a(); } "b" { c(); } { d(); } "e" { f(); };
```
is translated into:
```c
$@1: %empty { a(); };
$@2: %empty { c(); };
$@3: %empty { d(); };
exp: $@1 "b" $@2 $@3 "e" { f(); };
```
with new nonterminal symbols $@n, where n is a number.

A midrule action is expected to generate a value if it uses $$, or the (final) action uses $n where n denote the midrule action. In that case its nonterminal is rather named @n:
```c
exp: { a(); } "b" { $$ = c(); } { d(); } "e" { f = $1; };
```
is translated into
```c
@1: %empty { a(); };
@2: %empty { $$ = c(); };
$@3: %empty { d(); };
exp: @1 "b" @2 $@3 "e" { f = $1; }
```
There are probably two errors in the above example: the first midrule action does not generate a value (it does not use $$ although the final action uses it), and the value of the second one is not used (the final action does not use $3). Bison reports these errors when the midrule-value warnings are enabled (see Invoking Bison):
```c
$ bison -Wmidrule-value mid.y
mid.y:2.6-13: warning: unset value: $$
    2 | exp: { a(); } "b" { $$ = c(); } { d(); } "e" { f = $1; };
      |      ^~~~~~~~
mid.y:2.19-31: warning: unused value: $3
    2 | exp: { a(); } "b" { $$ = c(); } { d(); } "e" { f = $1; };
      |                   ^~~~~~~~~~~~~
```
It is sometimes useful to turn midrule actions into regular actions, e.g., to factor them, or to escape from their limitations. For instance, as an alternative to typed midrule action, you may bury the midrule action inside a nonterminal symbol and to declare a printer and a destructor for that symbol:
```c
%nterm <context> let
%destructor { pop_context ($$); } let
%printer { print_context (yyo, $$); } let

%%

stmt:
  let stmt
    {
      $$ = $2;
      pop_context ($let);
    };

let:
  "let" '(' var ')'
    {
      $let = push_context ();
      declare_variable ($var);
    };
```

#### 3.4.8.4 Conflicts due to Midrule Actions
Taking action before a rule is completely recognized often leads to conflicts since the parser must commit to a parse in order to execute the action. For example, the following two rules, without midrule actions, can coexist in a working parser because the parser can shift the open-brace token and look at what follows before deciding whether there is a declaration or not:
```c
compound:
  '{' declarations statements '}'
| '{' statements '}'
;
```
But when we add a midrule action as follows, the rules become nonfunctional:
```c
compound:
  { prepare_for_local_variables (); }
     '{' declarations statements '}'
|    '{' statements '}'
;
```
Now the parser is forced to decide whether to run the midrule action when it has read no farther than the open-brace. In other words, it must commit to using one rule or the other, without sufficient information to do it correctly. (The open-brace token is what is called the lookahead token at this time, since the parser is still deciding what to do about it. See Lookahead Tokens.)

You might think that you could correct the problem by putting identical actions into the two rules, like this:
```c
compound:
  { prepare_for_local_variables (); }
    '{' declarations statements '}'
| { prepare_for_local_variables (); }
    '{' statements '}'
;
```
But this does not help, because Bison does not realize that the two actions are identical. (Bison never tries to understand the C code in an action.)

If the grammar is such that a declaration can be distinguished from a statement by the first token (which is true in C), then one solution which does work is to put the action after the open-brace, like this:
```c
compound:
  '{' { prepare_for_local_variables (); }
    declarations statements '}'
| '{' statements '}'
;
```
Now the first token of the following declaration or statement, which would in any case tell Bison which rule to use, can still do so.

Another solution is to bury the action inside a nonterminal symbol which serves as a subroutine:
```c
subroutine:
  %empty  { prepare_for_local_variables (); }
;

compound:
  subroutine '{' declarations statements '}'
| subroutine '{' statements '}'
;
```
Now Bison can execute the action in the rule for subroutine without deciding which rule for compound it will eventually use.

## 3.5 Tracking Locations
Though grammar rules and semantic actions are enough to write a fully functional parser, it can be useful to process some additional information, especially symbol locations.

The way locations are handled is defined by providing a data type, and actions to take when rules are matched.

### 3.5.1 Data Type of Locations
Defining a data type for locations is much simpler than for semantic values, since all tokens and groupings always use the same type. The location type is specified using ‘%define api.location.type’:
```c
%define api.location.type {location_t}
```
This defines, in the C generated code, the YYLTYPE type name. When YYLTYPE is not defined, Bison uses a default structure type with four members:
```c
typedef struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
} YYLTYPE;
```
In C, you may also specify the type of locations by defining a macro called YYLTYPE, just as you can specify the semantic value type by defining a YYSTYPE macro (see Data Types of Semantic Values). However, rather than using macros, we recommend the api.value.type and api.location.type %define variables.

Default locations represent a range in the source file(s), but this is not a requirement. It could be a single point or just a line number, or even more complex structures.

When the default location type is used, Bison initializes all these fields to 1 for yylloc at the beginning of the parsing. To initialize yylloc with a custom location type (or to chose a different initialization), use the %initial-action directive. See Performing Actions before Parsing.

### 3.5.2 Actions and Locations
Actions are not only useful for defining language semantics, but also for describing the behavior of the output parser with locations.

The most obvious way for building locations of syntactic groupings is very similar to the way semantic values are computed. In a given rule, several constructs can be used to access the locations of the elements being matched. The location of the nth component of the right hand side is @n, while the location of the left hand side grouping is @$.

In addition, the named references construct @name and @[name] may also be used to address the symbol locations. See Named References, for more information about using the named references construct.

Here is a basic example using the default data type for locations:
```c
exp:
  …
| exp '/' exp
    {
      @$.first_column = @1.first_column;
      @$.first_line = @1.first_line;
      @$.last_column = @3.last_column;
      @$.last_line = @3.last_line;
      if ($3)
        $$ = $1 / $3;
      else
        {
          $$ = 1;
          fprintf (stderr, "%d.%d-%d.%d: division by zero",
                   @3.first_line, @3.first_column,
                   @3.last_line, @3.last_column);
        }
    }
```
As for semantic values, there is a default action for locations that is run each time a rule is matched. It sets the beginning of @$ to the beginning of the first symbol, and the end of @$ to the end of the last symbol.

With this default action, the location tracking can be fully automatic. The example above simply rewrites this way:
```c
exp:
  …
| exp '/' exp
    {
      if ($3)
        $$ = $1 / $3;
      else
        {
          $$ = 1;
          fprintf (stderr, "%d.%d-%d.%d: division by zero",
                   @3.first_line, @3.first_column,
                   @3.last_line, @3.last_column);
        }
    }
```
It is also possible to access the location of the lookahead token, if any, from a semantic action. This location is stored in yylloc. See Special Features for Use in Actions.

### 3.5.3 Printing Locations
When using the default location type, the debug traces report the symbols’ location. The generated parser does so using the YYLOCATION_PRINT macro.

**Macro: YYLOCATION_PRINT (file, loc);**  
When traces are enabled, print loc (of type ‘YYLTYPE const *’) on file (of type ‘FILE *’). Do nothing when traces are disabled, or if the location type is user defined.

To get locations in the debug traces with your user-defined location types, define the YYLOCATION_PRINT macro. For instance:
```c
#define YYLOCATION_PRINT   location_print
```

### 3.5.4 Default Action for Locations
Actually, actions are not the best place to compute locations. Since locations are much more general than semantic values, there is room in the output parser to redefine the default action to take for each rule. The YYLLOC_DEFAULT macro is invoked each time a rule is matched, before the associated action is run. It is also invoked while processing a syntax error, to compute the error’s location. Before reporting an unresolvable syntactic ambiguity, a GLR parser invokes YYLLOC_DEFAULT recursively to compute the location of that ambiguity.

Most of the time, this macro is general enough to suppress location dedicated code from semantic actions.

The YYLLOC_DEFAULT macro takes three parameters. The first one is the location of the grouping (the result of the computation). When a rule is matched, the second parameter identifies locations of all right hand side elements of the rule being matched, and the third parameter is the size of the rule’s right hand side. When a GLR parser reports an ambiguity, which of multiple candidate right hand sides it passes to YYLLOC_DEFAULT is undefined. When processing a syntax error, the second parameter identifies locations of the symbols that were discarded during error processing, and the third parameter is the number of discarded symbols.

By default, YYLLOC_DEFAULT is defined this way:
```c
# define YYLLOC_DEFAULT(Cur, Rhs, N)                      \
do                                                        \
  if (N)                                                  \
    {                                                     \
      (Cur).first_line   = YYRHSLOC(Rhs, 1).first_line;   \
      (Cur).first_column = YYRHSLOC(Rhs, 1).first_column; \
      (Cur).last_line    = YYRHSLOC(Rhs, N).last_line;    \
      (Cur).last_column  = YYRHSLOC(Rhs, N).last_column;  \
    }                                                     \
  else                                                    \
    {                                                     \
      (Cur).first_line   = (Cur).last_line   =            \
        YYRHSLOC(Rhs, 0).last_line;                       \
      (Cur).first_column = (Cur).last_column =            \
        YYRHSLOC(Rhs, 0).last_column;                     \
    }                                                     \
while (0)
```
where YYRHSLOC (rhs, k) is the location of the kth symbol in rhs when k is positive, and the location of the symbol just before the reduction when k and n are both zero.

When defining YYLLOC_DEFAULT, you should consider that:

- All arguments are free of side-effects. However, only the first one (the result) should be modified by YYLLOC_DEFAULT.
- For consistency with semantic actions, valid indexes within the right hand side range from 1 to n. When n is zero, only 0 is a valid index, and it refers to the symbol just before the reduction. During error processing n is always positive.
- Your macro should parenthesize its arguments, if need be, since the actual arguments may not be surrounded by parentheses. Also, your macro should expand to something that can be used as a single statement when it is followed by a semicolon.

## 3.6 Named References
As described in the preceding sections, the traditional way to refer to any semantic value or location is a positional reference, which takes the form $n, $$, @n, and @$. However, such a reference is not very descriptive. Moreover, if you later decide to insert or remove symbols in the right-hand side of a grammar rule, the need to renumber such references can be tedious and error-prone.

To avoid these issues, you can also refer to a semantic value or location using a named reference. First of all, original symbol names may be used as named references. For example:
```c
invocation: op '(' args ')'
  { $invocation = new_invocation ($op, $args, @invocation); }
```
Positional and named references can be mixed arbitrarily. For example:
```c
invocation: op '(' args ')'
  { $$ = new_invocation ($op, $args, @$); }
```
However, sometimes regular symbol names are not sufficient due to ambiguities:
```c
exp: exp '/' exp
  { $exp = $exp / $exp; } // $exp is ambiguous.

exp: exp '/' exp
  { $$ = $1 / $exp; } // One usage is ambiguous.

exp: exp '/' exp
  { $$ = $1 / $3; } // No error.
```
When ambiguity occurs, explicitly declared names may be used for values and locations. Explicit names are declared as a bracketed name after a symbol appearance in rule definitions. For example:
```c
exp[result]: exp[left] '/' exp[right]
  { $result = $left / $right; }
```
In order to access a semantic value generated by a midrule action, an explicit name may also be declared by putting a bracketed name after the closing brace of the midrule action code:
```c
exp[res]: exp[x] '+' {$left = $x;}[left] exp[right]
  { $res = $left + $right; }
```
In references, in order to specify names containing dots and dashes, an explicit bracketed syntax $[name] and @[name] must be used:
```c
if-stmt: "if" '(' expr ')' "then" then.stmt ';'
  { $[if-stmt] = new_if_stmt ($expr, $[then.stmt]); }
```
It often happens that named references are followed by a dot, dash or other C punctuation marks and operators. By default, Bison will read ‘$name.suffix’ as a reference to symbol value $name followed by ‘.suffix’, i.e., an access to the suffix field of the semantic value. In order to force Bison to recognize ‘name.suffix’ in its entirety as the name of a semantic value, the bracketed syntax ‘$[name.suffix]’ must be used.

## 3.7 Bison Declarations
The Bison declarations section of a Bison grammar defines the symbols used in formulating the grammar and the data types of semantic values. See Symbols, Terminal and Nonterminal.

All token kind names (but not single-character literal tokens such as '+' and '*') must be declared. Nonterminal symbols must be declared if you need to specify which data type to use for the semantic value (see More Than One Value Type).

The first rule in the grammar file also specifies the start symbol, by default. If you want some other symbol to be the start symbol, you must declare it explicitly (see Languages and Context-Free Grammars).

### 3.7.1 Require a Version of Bison
You may require the minimum version of Bison to process the grammar. If the requirement is not met, bison exits with an error (exit status 63).
```
%require "version"
```
Some deprecated behaviors are disabled for some required version:

"3.2" (or better)
The C++ deprecated files position.hh and stack.hh are no longer generated.

### 3.7.2 Token Kind Names
The basic way to declare a token kind name (terminal symbol) is as follows:

%token name
Bison will convert this into a definition in the parser, so that the function yylex (if it is in this file) can use the name name to stand for this token kind’s code.

Alternatively, you can use %left, %right, %precedence, or %nonassoc instead of %token, if you wish to specify associativity and precedence. See Operator Precedence. However, for clarity, we recommend to use these directives only to declare associativity and precedence, and not to add string aliases, semantic types, etc.

You can explicitly specify the numeric code for a token kind by appending a nonnegative decimal or hexadecimal integer value in the field immediately following the token name:
```c
%token NUM 300
%token XNUM 0x12d // a GNU extension
```
It is generally best, however, to let Bison choose the numeric codes for all token kinds. Bison will automatically select codes that don’t conflict with each other or with normal characters.

In the event that the stack type is a union, you must augment the %token or other token declaration to include the data type alternative delimited by angle-brackets (see More Than One Value Type).

For example:
```c
%union {              /* define stack type */
  double val;
  symrec *tptr;
}
%token <val> NUM      /* define token NUM and its type */
```
You can associate a literal string token with a token kind name by writing the literal string at the end of a %token declaration which declares the name. For example:
```c
%token ARROW "=>"
```
For example, a grammar for the C language might specify these names with equivalent literal string tokens:
```c
%token  <operator>  OR      "||"
%token  <operator>  LE 134  "<="
%left  OR  "<="
```
Once you equate the literal string and the token kind name, you can use them interchangeably in further declarations or the grammar rules. The yylex function can use the token name or the literal string to obtain the token kind code (see Calling Convention for yylex).

String aliases allow for better error messages using the literal strings instead of the token names, such as ‘syntax error, unexpected ||, expecting number or (’ rather than ‘syntax error, unexpected OR, expecting NUM or LPAREN’.

String aliases may also be marked for internationalization (see Token Internationalization):
```c
%token
    OR     "||"
    LPAREN "("
    RPAREN ")"
    '\n'   _("end of line")
  <double>
    NUM    _("number")
```
would produce in French ‘erreur de syntaxe, || inattendu, attendait nombre ou (’ rather than ‘erreur de syntaxe, || inattendu, attendait number ou (’.


### 3.7.3 Operator Precedence
Use the %left, %right, %nonassoc, or %precedence declaration to declare a token and specify its precedence and associativity, all at once. These are called precedence declarations. See Operator Precedence, for general information on operator precedence.

The syntax of a precedence declaration is nearly the same as that of %token: either
```c
%left symbols…
```
or
```c
%left <type> symbols…
```
And indeed any of these declarations serves the purposes of %token. But in addition, they specify the associativity and relative precedence for all the symbols:

The associativity of an operator op determines how repeated uses of the operator nest: whether ‘x op y op z’ is parsed by grouping x with y first or by grouping y with z first. %left specifies left-associativity (grouping x with y first) and %right specifies right-associativity (grouping y with z first). %nonassoc specifies no associativity, which means that ‘x op y op z’ is considered a syntax error.
%precedence gives only precedence to the symbols, and defines no associativity at all. Use this to define precedence only, and leave any potential conflict due to associativity enabled.

The precedence of an operator determines how it nests with other operators. All the tokens declared in a single precedence declaration have equal precedence and nest together according to their associativity. When two tokens declared in different precedence declarations associate, the one declared later has the higher precedence and is grouped first.
For backward compatibility, there is a confusing difference between the argument lists of %token and precedence declarations. Only a %token can associate a literal string with a token kind name. A precedence declaration always interprets a literal string as a reference to a separate token. For example:
```c
%left  OR "<="         // Does not declare an alias.
%left  OR 134 "<=" 135 // Declares 134 for OR and 135 for "<=".
```

### 3.7.4 Nonterminal Symbols
When you use %union to specify multiple value types, you must declare the value type of each nonterminal symbol for which values are used. This is done with a %type declaration, like this:
```c
%type <type> nonterminal…
```
Here nonterminal is the name of a nonterminal symbol, and type is the name given in the %union to the alternative that you want (see The Union Declaration). You can give any number of nonterminal symbols in the same %type declaration, if they have the same value type. Use spaces to separate the symbol names.

While POSIX Yacc allows %type only for nonterminals, Bison accepts that this directive be also applied to terminal symbols. To declare exclusively nonterminal symbols, use the safer %nterm:
```c
%nterm <type> nonterminal…
```

### 3.7.5 Syntax of Symbol Declarations
The syntax of the various directives to declare symbols is as follows.
```c
%token tag? ( id number? string? )+ ( tag ( id number? string? )+ )*
%left  tag? ( id number?)+ ( tag ( id number? )+ )*
%type  tag? ( id | char | string )+ ( tag ( id | char | string )+ )*
%nterm tag? id+ ( tag id+ )*
```
where tag denotes a type tag such as ‘<ival>’, id denotes an identifier such as ‘NUM’, number a decimal or hexadecimal integer such as ‘300’ or ‘0x12d’, char a character literal such as ‘'+'’, and string a string literal such as ‘"number"’. The postfix quantifiers are ‘?’ (zero or one), ‘*’ (zero or more) and ‘+’ (one or more).

The directives %precedence, %right and %nonassoc behave like %left.

### 3.7.6 Performing Actions before Parsing
Sometimes your parser needs to perform some initializations before parsing. The %initial-action directive allows for such arbitrary code.
```c
Directive: %initial-action { code }
```
Declare that the braced code must be invoked before parsing each time yyparse is called. The code may use $$ (or $<tag>$) and @$ — initial value and location of the lookahead — and the %parse-param.

For instance, if your locations use a file name, you may use
```c
%parse-param { char const *file_name };
%initial-action
{
  @$.initialize (file_name);
};
```

### 3.7.7 Freeing Discarded Symbols
During error recovery (see Error Recovery), symbols already pushed on the stack and tokens coming from the rest of the file are discarded until the parser falls on its feet. If the parser runs out of memory, or if it returns via YYABORT, YYACCEPT or YYNOMEM, all the symbols on the stack must be discarded. Even if the parser succeeds, it must discard the start symbol.

When discarded symbols convey heap based information, this memory is lost. While this behavior can be tolerable for batch parsers, such as in traditional compilers, it is unacceptable for programs like shells or protocol implementations that may parse and execute indefinitely.

The %destructor directive defines code that is called when a symbol is automatically discarded.
```c
Directive: %destructor { code } symbols
```
Invoke the braced code whenever the parser discards one of the symbols. Within code, $$ (or $<tag>$) designates the semantic value associated with the discarded symbol, and @$ designates its location. The additional parser parameters are also available (see The Parser Function yyparse).

When a symbol is listed among symbols, its %destructor is called a per-symbol %destructor. You may also define a per-type %destructor by listing a semantic type tag among symbols. In that case, the parser will invoke this code whenever it discards any grammar symbol that has that semantic type tag unless that symbol has its own per-symbol %destructor.

Finally, you can define two different kinds of default %destructors. You can place each of <*> and <> in the symbols list of exactly one %destructor declaration in your grammar file. The parser will invoke the code associated with one of these whenever it discards any user-defined grammar symbol that has no per-symbol and no per-type %destructor. The parser uses the code for <*> in the case of such a grammar symbol for which you have formally declared a semantic type tag (%token, %nterm, and %type count as such a declaration, but $<tag>$ does not). The parser uses the code for <> in the case of such a grammar symbol that has no declared semantic type tag.

For example:
```c
%union { char *string; }
%token <string> STRING1 STRING2
%nterm <string> string1 string2
%union { char character; }
%token <character> CHR
%nterm <character> chr
%token TAGLESS

%destructor { } <character>
%destructor { free ($$); } <*>
%destructor { free ($$); printf ("%d", @$.first_line); } STRING1 string1
%destructor { printf ("Discarding tagless symbol.\n"); } <>
```
guarantees that, when the parser discards any user-defined symbol that has a semantic type tag other than <character>, it passes its semantic value to free by default. However, when the parser discards a STRING1 or a string1, it uses the third %destructor, which frees it and prints its line number to stdout (free is invoked only once). Finally, the parser merely prints a message whenever it discards any symbol, such as TAGLESS, that has no semantic type tag.

A Bison-generated parser invokes the default %destructors only for user-defined as opposed to Bison-defined symbols. For example, the parser will not invoke either kind of default %destructor for the special Bison-defined symbols $accept, $undefined, or $end (see Bison Symbols), none of which you can reference in your grammar. It also will not invoke either for the error token (see Bison Symbols), which is always defined by Bison regardless of whether you reference it in your grammar. However, it may invoke one of them for the end token (token 0) if you redefine it from $end to, for example, END:
```c
%token END 0
```
Finally, Bison will never invoke a %destructor for an unreferenced midrule semantic value (see Actions in Midrule). That is, Bison does not consider a midrule to have a semantic value if you do not reference $$ in the midrule’s action or $n (where n is the right-hand side symbol position of the midrule) in any later action in that rule. However, if you do reference either, the Bison-generated parser will invoke the <> %destructor whenever it discards the midrule symbol.


Discarded symbols are the following:

- stacked symbols popped during the first phase of error recovery,
- incoming terminals during the second phase of error recovery,
- the current lookahead and the entire stack (except the current right-hand side symbols) when the parser returns immediately, and
- the current lookahead and the entire stack (including the current right-hand side symbols) when the C++ parser (lalr1.cc) catches an exception in parse,
- the start symbol, when the parser succeeds.

The parser can return immediately because of an explicit call to YYABORT, YYACCEPT or YYNOMEM, or failed error recovery, or memory exhaustion.

Right-hand side symbols of a rule that explicitly triggers a syntax error via YYERROR are not discarded automatically. As a rule of thumb, destructors are invoked only when user actions cannot manage the memory.

### 3.7.8 Printing Semantic Values
When run-time traces are enabled (see Tracing Your Parser), the parser reports its actions, such as reductions. When a symbol involved in an action is reported, only its kind is displayed, as the parser cannot know how semantic values should be formatted.

The %printer directive defines code that is called when a symbol is reported. Its syntax is the same as %destructor (see Freeing Discarded Symbols).

Directive: %printer { code } symbols
Invoke the braced code whenever the parser displays one of the symbols. Within code, yyo denotes the output stream (a FILE* in C, an std::ostream& in C++, and stdout in D), $$ (or $<tag>$) designates the semantic value associated with the symbol, and @$ its location. The additional parser parameters are also available (see The Parser Function yyparse).

The symbols are defined as for %destructor (see Freeing Discarded Symbols.): they can be per-type (e.g., ‘<ival>’), per-symbol (e.g., ‘exp’, ‘NUM’, ‘"float"’), typed per-default (i.e., ‘<*>’, or untyped per-default (i.e., ‘<>’).

For example:
```c
%union { char *string; }
%token <string> STRING1 STRING2
%nterm <string> string1 string2
%union { char character; }
%token <character> CHR
%nterm <character> chr
%token TAGLESS

%printer { fprintf (yyo, "'%c'", $$); } <character>
%printer { fprintf (yyo, "&%p", $$); } <*>
%printer { fprintf (yyo, "\"%s\"", $$); } STRING1 string1
%printer { fprintf (yyo, "<>"); } <>
```
guarantees that, when the parser print any symbol that has a semantic type tag other than <character>, it display the address of the semantic value by default. However, when the parser displays a STRING1 or a string1, it formats it as a string in double quotes. It performs only the second %printer in this case, so it prints only once. Finally, the parser print ‘<>’ for any symbol, such as TAGLESS, that has no semantic type tag. See Enabling Debug Traces for mfcalc, for a complete example.

### 3.7.9 Suppressing Conflict Warnings
Bison normally warns if there are any conflicts in the grammar (see Shift/Reduce Conflicts), but most real grammars have harmless shift/reduce conflicts which are resolved in a predictable way and would be difficult to eliminate. It is desirable to suppress the warning about these conflicts unless the number of conflicts changes. You can do this with the %expect declaration.

The declaration looks like this:
```c
%expect n
```
Here n is a decimal integer. The declaration says there should be n shift/reduce conflicts and no reduce/reduce conflicts. Bison reports an error if the number of shift/reduce conflicts differs from n, or if there are any reduce/reduce conflicts.

For deterministic parsers, reduce/reduce conflicts are more serious, and should be eliminated entirely. Bison will always report reduce/reduce conflicts for these parsers. With GLR parsers, however, both kinds of conflicts are routine; otherwise, there would be no need to use GLR parsing. Therefore, it is also possible to specify an expected number of reduce/reduce conflicts in GLR parsers, using the declaration:
```c
%expect-rr n
```
You may wish to be more specific in your specification of expected conflicts. To this end, you can also attach %expect and %expect-rr modifiers to individual rules. The interpretation of these modifiers differs from their use as declarations. When attached to rules, they indicate the number of states in which the rule is involved in a conflict. You will need to consult the output resulting from -v to determine appropriate numbers to use. For example, for the following grammar fragment, the first rule for empty_dims appears in two states in which the ‘[’ token is a lookahead. Having determined that, you can document this fact with an %expect modifier as follows:
```c
dims:
  empty_dims
| '[' expr ']' dims
;

empty_dims:
  %empty   %expect 2
| empty_dims '[' ']'
;
```
Mid-rule actions generate implicit rules that are also subject to conflicts (see Conflicts due to Midrule Actions). To attach an %expect or %expect-rr annotation to an implicit mid-rule action’s rule, put it before the action. For example,
```c
%glr-parser
%expect-rr 1

%%

clause:
  "condition" %expect-rr 1 { value_mode(); } '(' exprs ')'
| "condition" %expect-rr 1 { class_mode(); } '(' types ')'
;
```
Here, the appropriate mid-rule action will not be determined until after the ‘(’ token is shifted. Thus, the two actions will clash with each other, and we should expect one reduce/reduce conflict for each.

In general, using %expect involves these steps:

- Compile your grammar without %expect. Use the -v option to get a verbose list of where the conflicts occur. Bison will also print the number of conflicts.
- Check each of the conflicts to make sure that Bison’s default resolution is what you really want. If not, rewrite the grammar and go back to the beginning.
- Add an %expect declaration, copying the number n from the number that Bison printed. With GLR parsers, add an %expect-rr declaration as well.
- Optionally, count up the number of states in which one or more conflicted reductions for particular rules appear and add these numbers to the affected rules as %expect-rr or %expect modifiers as appropriate. Rules that are in conflict appear in the output listing surrounded by square brackets or, in the case of reduce/reduce conflicts, as reductions having the same lookahead symbol as a square-bracketed reduction in the same state.

Now Bison will report an error if you introduce an unexpected conflict, but will keep silent otherwise.

### 3.7.10 The Start-Symbol
Bison assumes by default that the start symbol for the grammar is the first nonterminal specified in the grammar specification section. The programmer may override this restriction with the %start declaration as follows:
```c
%start symbol
```
### 3.7.11 A Pure (Reentrant) Parser
A reentrant program is one which does not alter in the course of execution; in other words, it consists entirely of pure (read-only) code. Reentrancy is important whenever asynchronous execution is possible; for example, a nonreentrant program may not be safe to call from a signal handler. In systems with multiple threads of control, a nonreentrant program must be called only within interlocks.

Normally, Bison generates a parser which is not reentrant. This is suitable for most uses, and it permits compatibility with Yacc. (The standard Yacc interfaces are inherently nonreentrant, because they use statically allocated variables for communication with yylex, including yylval and yylloc.)

Alternatively, you can generate a pure, reentrant parser. The Bison declaration ‘%define api.pure’ says that you want the parser to be reentrant. It looks like this:
```c
%define api.pure full
```
The result is that the communication variables yylval and yylloc become local variables in yyparse, and a different calling convention is used for the lexical analyzer function yylex. See Calling Conventions for Pure Parsers, for the details of this. The variable yynerrs becomes local in yyparse in pull mode but it becomes a member of yypstate in push mode. (see The Error Reporting Function yyerror). The convention for calling yyparse itself is unchanged.

Whether the parser is pure has nothing to do with the grammar rules. You can generate either a pure parser or a nonreentrant parser from any valid grammar.

### 3.7.12 A Push Parser
A pull parser is called once and it takes control until all its input is completely parsed. A push parser, on the other hand, is called each time a new token is made available.

A push parser is typically useful when the parser is part of a main event loop in the client’s application. This is typically a requirement of a GUI, when the main event loop needs to be triggered within a certain time period.

Normally, Bison generates a pull parser. The following Bison declaration says that you want the parser to be a push parser (see %define Summary):
```c
%define api.push-pull push
```
In almost all cases, you want to ensure that your push parser is also a pure parser (see A Pure (Reentrant) Parser). The only time you should create an impure push parser is to have backwards compatibility with the impure Yacc pull mode interface. Unless you know what you are doing, your declarations should look like this:
```c
%define api.pure full
%define api.push-pull push
```
There is a major notable functional difference between the pure push parser and the impure push parser. It is acceptable for a pure push parser to have many parser instances, of the same type of parser, in memory at the same time. An impure push parser should only use one parser at a time.

When a push parser is selected, Bison will generate some new symbols in the generated parser. yypstate is a structure that the generated parser uses to store the parser’s state. yypstate_new is the function that will create a new parser instance. yypstate_delete will free the resources associated with the corresponding parser instance. Finally, yypush_parse is the function that should be called whenever a token is available to provide the parser. A trivial example of using a pure push parser would look like this:
```c
int status;
yypstate *ps = yypstate_new ();
do {
  status = yypush_parse (ps, yylex (), NULL);
} while (status == YYPUSH_MORE);
yypstate_delete (ps);
```
If the user decided to use an impure push parser, a few things about the generated parser will change. The yychar variable becomes a global variable instead of a local one in the yypush_parse function. For this reason, the signature of the yypush_parse function is changed to remove the token as a parameter. A nonreentrant push parser example would thus look like this:
```c
extern int yychar;
int status;
yypstate *ps = yypstate_new ();
do {
  yychar = yylex ();
  status = yypush_parse (ps);
} while (status == YYPUSH_MORE);
yypstate_delete (ps);
```
That’s it. Notice the next token is put into the global variable yychar for use by the next invocation of the yypush_parse function.

Bison also supports both the push parser interface along with the pull parser interface in the same generated parser. In order to get this functionality, you should replace the ‘%define api.push-pull push’ declaration with the ‘%define api.push-pull both’ declaration. Doing this will create all of the symbols mentioned earlier along with the two extra symbols, yyparse and yypull_parse. yyparse can be used exactly as it normally would be used. However, the user should note that it is implemented in the generated parser by calling yypull_parse. This makes the yyparse function that is generated with the ‘%define api.push-pull both’ declaration slower than the normal yyparse function. If the user calls the yypull_parse function it will parse the rest of the input stream. It is possible to yypush_parse tokens to select a subgrammar and then yypull_parse the rest of the input stream. If you would like to switch back and forth between between parsing styles, you would have to write your own yypull_parse function that knows when to quit looking for input. An example of using the yypull_parse function would look like this:
```c
yypstate *ps = yypstate_new ();
yypull_parse (ps); /* Will call the lexer */
yypstate_delete (ps);
```
Adding the ‘%define api.pure’ declaration does exactly the same thing to the generated parser with ‘%define api.push-pull both’ as it did for ‘%define api.push-pull push’.

### 3.7.13 Bison Declaration Summary
Here is a summary of the declarations used to define a grammar:

- Directive: %union  
Declare the collection of data types that semantic values may have (see The Union Declaration).

- Directive: %token  
Declare a terminal symbol (token kind name) with no precedence or associativity specified (see Token Kind Names).

- Directive: %right  
Declare a terminal symbol (token kind name) that is right-associative (see Operator Precedence).

- Directive: %left  
Declare a terminal symbol (token kind name) that is left-associative (see Operator Precedence).

- Directive: %nonassoc  
Declare a terminal symbol (token kind name) that is nonassociative (see Operator Precedence). Using it in a way that would be associative is a syntax error.

- Directive: %nterm  
Declare the type of semantic values for a nonterminal symbol (see Nonterminal Symbols).

- Directive: %type  
Declare the type of semantic values for a symbol (see Nonterminal Symbols).

- Directive: %start  
Specify the grammar’s start symbol (see The Start-Symbol).

- Directive: %expect  
Declare the expected number of shift/reduce conflicts, either overall or for a given rule (see Suppressing Conflict Warnings).

- Directive: %expect-rr  
Declare the expected number of reduce/reduce conflicts, either overall or for a given rule (see Suppressing Conflict Warnings).


In order to change the behavior of bison, use the following directives:

- Directive: %code {code}  
- Directive: %code qualifier {code}  
Insert code verbatim into the output parser source at the default location or at the location specified by qualifier. See %code Summary.

- Directive: %debug  
Instrument the parser for traces. Obsoleted by ‘%define parse.trace’. See Tracing Your Parser.

- Directive: %define variable  
- Directive: %define variable value  
- Directive: %define variable {value}  
- Directive: %define variable "value"  
Define a variable to adjust Bison’s behavior. See %define Summary.

- Directive: %defines  
- Directive: %defines defines-file  
Historical name for %header. See %header.

- Directive: %destructor  
Specify how the parser should reclaim the memory associated to discarded symbols. See Freeing Discarded Symbols.

- Directive: %file-prefix "prefix"  
Specify a prefix to use for all Bison output file names. The names are chosen as if the grammar file were named prefix.y.

- Directive: %header  
Write a parser header file containing definitions for the token kind names defined in the grammar as well as a few other declarations. If the parser implementation file is named name.c then the parser header file is named name.h.

For C parsers, the parser header file declares YYSTYPE unless YYSTYPE is already defined as a macro or you have used a <type> tag without using %union. Therefore, if you are using a %union (see More Than One Value Type) with components that require other definitions, or if you have defined a YYSTYPE macro or type definition (see Data Types of Semantic Values), you need to arrange for these definitions to be propagated to all modules, e.g., by putting them in a prerequisite header that is included both by your parser and by any other module that needs YYSTYPE.

Unless your parser is pure, the parser header file declares yylval as an external variable. See A Pure (Reentrant) Parser.

If you have also used locations, the parser header file declares YYLTYPE and yylloc using a protocol similar to that of the YYSTYPE macro and yylval. See Tracking Locations.

This parser header file is normally essential if you wish to put the definition of yylex in a separate source file, because yylex typically needs to be able to refer to the above-mentioned declarations and to the token kind codes. See Semantic Values of Tokens.

If you have declared %code requires or %code provides, the output header also contains their code. See %code Summary.

The generated header is protected against multiple inclusions with a C preprocessor guard: ‘YY_PREFIX_FILE_INCLUDED’, where PREFIX and FILE are the prefix (see Multiple Parsers in the Same Program) and generated file name turned uppercase, with each series of non alphanumerical characters converted to a single underscore.

For instance with ‘%define api.prefix {calc}’ and ‘%header "lib/parse.h"’, the header will be guarded as follows.
```c
#ifndef YY_CALC_LIB_PARSE_H_INCLUDED
# define YY_CALC_LIB_PARSE_H_INCLUDED
...
#endif /* ! YY_CALC_LIB_PARSE_H_INCLUDED */
```
Introduced in Bison 3.8.

- Directive: %header header-file  
Same as above, but save in the file header-file.

- Directive: %language "language"  
Specify the programming language for the generated parser. Currently supported languages include C, C++, D and Java. language is case-insensitive.

- Directive: %locations  
Generate the code processing the locations (see Special Features for Use in Actions). This mode is enabled as soon as the grammar uses the special ‘@n’ tokens, but if your grammar does not use it, using ‘%locations’ allows for more accurate syntax error messages.

- Directive: %name-prefix "prefix"  
Obsoleted by ‘%define api.prefix {prefix}’. See Multiple Parsers in the Same Program. For C++ parsers, see the ‘%define api.namespace’ documentation in this section.

Rename the external symbols used in the parser so that they start with prefix instead of ‘yy’. The precise list of symbols renamed in C parsers is yyparse, yylex, yyerror, yynerrs, yylval, yychar, yydebug, and (if locations are used) yylloc. If you use a push parser, yypush_parse, yypull_parse, yypstate, yypstate_new and yypstate_delete will also be renamed. For example, if you use ‘%name-prefix "c_"’, the names become c_parse, c_lex, and so on.

Contrary to defining api.prefix, some symbols are not renamed by %name-prefix, for instance YYDEBUG, YYTOKENTYPE, yytoken_kind_t, YYSTYPE, YYLTYPE.

- Directive: %no-lines  
Don’t generate any #line preprocessor commands in the parser implementation file. Ordinarily Bison writes these commands in the parser implementation file so that the C compiler and debuggers will associate errors and object code with your source file (the grammar file). This directive causes them to associate errors with the parser implementation file, treating it as an independent source file in its own right.

- Directive: %output "file"  
Generate the parser implementation in file.

- Directive: %pure-parser  
Deprecated version of ‘%define api.pure’ (see %define Summary), for which Bison is more careful to warn about unreasonable usage.

- Directive: %require "version"  
Require version version or higher of Bison. See Require a Version of Bison.

- Directive: %skeleton "file"  
Specify the skeleton to use.

If file does not contain a /, file is the name of a skeleton file in the Bison installation directory. If it does, file is an absolute file name or a file name relative to the directory of the grammar file. This is similar to how most shells resolve commands.

- Directive: %token-table  
This feature is obsolescent, avoid it in new projects.

Generate an array of token names in the parser implementation file. The name of the array is yytname; yytname[i] is the name of the token whose internal Bison token code is i. The first three elements of yytname correspond to the predefined tokens "$end", "error", and "$undefined"; after these come the symbols defined in the grammar file.

The name in the table includes all the characters needed to represent the token in Bison. For single-character literals and literal strings, this includes the surrounding quoting characters and any escape sequences. For example, the Bison single-character literal '+' corresponds to a three-character name, represented in C as "'+'"; and the Bison two-character literal string "\\/" corresponds to a five-character name, represented in C as "\"\\\\/\"".

When you specify %token-table, Bison also generates macro definitions for macros YYNTOKENS, YYNNTS, and YYNRULES, and YYNSTATES:

YYNTOKENS  
The number of terminal symbols, i.e., the highest token code, plus one.

YYNNTS  
The number of nonterminal symbols.

YYNRULES  
The number of grammar rules,

YYNSTATES  
The number of parser states (see Parser States).

Here’s code for looking up a multicharacter token in yytname, assuming that the characters of the token are stored in token_buffer, and assuming that the token does not contain any characters like ‘"’ that require escaping.
```c
for (int i = 0; i < YYNTOKENS; i++)
  if (yytname[i]
      && yytname[i][0] == '"'
      && ! strncmp (yytname[i] + 1, token_buffer,
                    strlen (token_buffer))
      && yytname[i][strlen (token_buffer) + 1] == '"'
      && yytname[i][strlen (token_buffer) + 2] == 0)
    break;
```
This method is discouraged: the primary purpose of string aliases is forging good error messages, not describing the spelling of keywords. In addition, looking for the token kind at runtime incurs a (small but noticeable) cost.

Finally, %token-table is incompatible with the custom and detailed values of the parse.error %define variable.

- Directive: %verbose  
Write an extra output file containing verbose descriptions of the parser states and what is done for each type of lookahead token in that state. See Understanding Your Parser, for more information.

- Directive: %yacc  
Pretend the option --yacc was given (see --yacc), i.e., imitate Yacc, including its naming conventions. Only makes sense with the yacc.c skeleton. See Tuning the Parser, for more.

Of course, being a Bison extension, %yacc is somewhat self-contradictory…

### 3.7.14 %define Summary
There are many features of Bison’s behavior that can be controlled by assigning the feature a single value. For historical reasons, some such features are assigned values by dedicated directives, such as %start, which assigns the start symbol. However, newer such features are associated with variables, which are assigned by the %define directive:

Directive: %define variable  
Directive: %define variable value  
Directive: %define variable {value}  
Directive: %define variable "value"  
Define variable to value.

The type of the values depend on the syntax. Braces denote value in the target language (e.g., a namespace, a type, etc.). Keyword values (no delimiters) denote finite choice (e.g., a variation of a feature). String values denote remaining cases (e.g., a file name).

It is an error if a variable is defined by %define multiple times, but see -D name[=value].

The rest of this section summarizes variables and values that %define accepts.

Some variables take Boolean values. In this case, Bison will complain if the variable definition does not meet one of the following four conditions:

1. value is true
2. value is omitted (or "" is specified). This is equivalent to true.
3. value is false.
4. variable is never defined. In this case, Bison selects a default value.

What variables are accepted, as well as their meanings and default values, depend on the selected target language and/or the parser skeleton (see Bison Declaration Summary, see Bison Declaration Summary). Unaccepted variables produce an error. Some of the accepted variables are described below.

Directive: %define api.filename.type {type}  
- Language(s): C++
- Purpose: Define the type of file names in Bison’s default location and position types. See Exposing the Location Classes.
- Accepted Values: Any type that is printable (via streams) and comparable (with == and !=).
- Default Value: const std::string.
- History: Introduced in Bison 2.0 as filename_type (with std::string as default), renamed as api.filename.type in Bison 3.7 (with const std::string as default).

Directive: %define api.header.include {"header.h"}

Directive: %define api.header.include {<header.h>}

- Languages(s): C (yacc.c)
- Purpose: Specify how the generated parser should include the generated header.  
Historically, when option -d or --header was used, bison generated a header and pasted an exact copy of it into the generated parser implementation file. Since Bison 3.6, it is #included as ‘"basename.h"’, instead of duplicated, unless file is ‘y.tab’, see below.

The api.header.include variable allows to control how the generated parser #includes the generated header. For instance:
```c
%define api.header.include {"parse.h"}
```
or
```c
%define api.header.include {<parser/parse.h>}
```
Using api.header.include does not change the name of the generated header, only how it is included.

To work around limitations of Automake’s ylwrap (which runs bison with --yacc), api.header.include is not predefined when the output file is y.tab.c. Define it to avoid the duplication.

- Accepted Values: An argument for #include.
- Default Value: ‘"header-basename"’, unless the header file is y.tab.h, where header-basename is the name of the generated header, without directory part. For instance with ‘bison -d calc/parse.y’, api.header.include defaults to ‘"parse.h"’, not ‘"calc/parse.h"’.
- History: Introduced in Bison 3.4. Defaults to ‘"basename.h"’ since Bison 3.7, unless the header file is y.tab.h.

Directive: %define api.location.file "file"

Directive: %define api.location.file none
- Language(s): C++
- Purpose: Define the name of the file in which Bison’s default location and position types are generated. See Exposing the Location Classes.
- Accepted Values:  
none  
If locations are enabled, generate the definition of the position and location classes in the header file if %header, otherwise in the parser implementation.  
"file"  
Generate the definition of the position and location classes in file. This file name can be relative (to where the parser file is output) or absolute.

-  Default Value: Not applicable if locations are not enabled, or if a user location type is specified (see api.location.type). Otherwise, Bison’s location is generated in location.hh (see C++ location).
- History: Introduced in Bison 3.2.

Directive: %define api.location.include {"file"}

Directive: %define api.location.include {<file>}
- Language(s): C++
- Purpose: Specify how the generated file that defines the position and location classes is included. This makes sense when the location class is exposed to the rest of your application/library in another directory. See Exposing the Location Classes.
- Accepted Values: Argument for #include.
- Default Value: ‘"dir/location.hh"’ where dir is the directory part of the output. For instance src/parse if --output=src/parse/parser.cc was given.
- History: Introduced in Bison 3.2.

Directive: %define api.location.type {type}
- Language(s): C, C++, Java
- Purpose: Define the location type. See Data Type of Locations, and User Defined Location Type.
- Accepted Values: String
- Default Value: none
- History: Introduced in Bison 2.7 for C++ and Java, in Bison 3.4 for C. Was originally named location_type in Bison 2.5 and 2.6.

Directive: %define api.namespace {namespace}
- Languages(s): C++
- Purpose: Specify the namespace for the parser class. For example, if you specify:
%define api.namespace {foo::bar}
Bison uses foo::bar verbatim in references such as:
```c
foo::bar::parser::value_type
```
However, to open a namespace, Bison removes any leading :: and then splits on any remaining occurrences:
```
namespace foo { namespace bar {
  class position;
  class location;
} }
```
- Accepted Values: Any absolute or relative C++ namespace reference without a trailing "::". For example, "foo" or "::foo::bar".
- Default Value: yy, unless you used the obsolete ‘%name-prefix "prefix"’ directive.

Directive: %define api.parser.class {name}
- Language(s): C++, Java, D
- Purpose: The name of the parser class.
- Accepted Values: Any valid identifier.
- Default Value: In C++, parser. In D and Java, YYParser or api.prefixParser (see Java Bison Interface).
- History: Introduced in Bison 3.3 to replace parser_class_name.

Directive: %define api.prefix {prefix}
- Language(s): C, C++, Java
- Purpose: Rename exported symbols. See Multiple Parsers in the Same Program.
- Accepted Values: String
- Default Value: YY for Java, yy otherwise.
- History: introduced in Bison 2.6, with its argument in double quotes. Uses braces since Bison 3.0 (double quotes are still supported for backward compatibility).

Directive: %define api.pure purity
- Language(s): C
- Purpose: Request a pure (reentrant) parser program. See A Pure (Reentrant) Parser.
- Accepted Values: true, false, full
The value may be omitted: this is equivalent to specifying true, as is the case for Boolean values.

When %define api.pure full is used, the parser is made reentrant. This changes the signature for yylex (see Calling Conventions for Pure Parsers), and also that of yyerror when the tracking of locations has been activated, as shown below.

The true value is very similar to the full value, the only difference is in the signature of yyerror on Yacc parsers without %parse-param, for historical reasons.

I.e., if ‘%locations %define api.pure’ is passed then the prototypes for yyerror are:
```c
void yyerror (char const *msg);                 // Yacc parsers.
void yyerror (YYLTYPE *locp, char const *msg);  // GLR parsers.
```
But if ‘%locations %define api.pure %parse-param {int *nastiness}’ is used, then both parsers have the same signature:
```
void yyerror (YYLTYPE *llocp, int *nastiness, char const *msg);
(see The Error Reporting Function yyerror)
```
- Default Value: false
- History: the full value was introduced in Bison 2.7

Directive: %define api.push-pull kind
- Language(s): C (deterministic parsers only), D, Java
- Purpose: Request a pull parser, a push parser, or both. See A Push Parser.
- Accepted Values: pull, push, both
- Default Value: pull

Directive: %define api.symbol.prefix {prefix}
- Languages(s): all
- Purpose: Add a prefix to the name of the symbol kinds. For instance
```c
%define api.symbol.prefix {S_}
%token FILE for ERROR
%%
start: FILE for ERROR;
```
generates this definition in C:
```c
/* Symbol kind.  */
enum yysymbol_kind_t
{
  S_YYEMPTY = -2,   /* No symbol.  */
  S_YYEOF = 0,      /* $end  */
  S_YYERROR = 1,    /* error  */
  S_YYUNDEF = 2,    /* $undefined  */
  S_FILE = 3,       /* FILE  */
  S_for = 4,        /* for  */
  S_ERROR = 5,      /* ERROR  */
  S_YYACCEPT = 6,   /* $accept  */
  S_start = 7       /* start  */
};
```
- Accepted Values: Any non empty string. Must be a valid identifier in the target language (typically a non empty sequence of letters, underscores, and —not at the beginning— digits).
The empty prefix is (generally) invalid:

in C it would create collision with the YYERROR macro, and potentially token kind definitions and symbol kind definitions would collide;  
unnamed symbols (such as ‘'+'’) have a name which starts with a digit;  
even in languages with scoped enumerations such as Java, an empty prefix is dangerous: symbol names may collide with the target language keywords, or with other members of the SymbolKind class.
- Default Value: YYSYMBOL_ in C, S_ in C++ and Java, empty in D.
History: introduced in Bison 3.6.

Directive: %define api.token.constructor
- Language(s): C++, D
- Purpose: Request that symbols be handled as a whole (type, value, and possibly location) in the scanner. In the case of C++, it works only when variant-based semantic values are enabled (see C++ Variants), see Complete Symbols, for details. In D, token constructors work with both ‘%union’ and ‘%define api.value.type union’.
- Accepted Values: Boolean.
- Default Value: false
- History: introduced in Bison 3.0.

Directive: %define api.token.prefix {prefix}
- Languages(s): all
- Purpose: Add a prefix to the token names when generating their definition in the target language. For instance
```
%define api.token.prefix {TOK_}
%token FILE for ERROR
%%
start: FILE for ERROR;
```
generates the definition of the symbols TOK_FILE, TOK_for, and TOK_ERROR in the generated source files. In particular, the scanner must use these prefixed token names, while the grammar itself may still use the short names (as in the sample rule given above). The generated informational files (*.output, *.xml, *.gv) are not modified by this prefix.

Bison also prefixes the generated member names of the semantic value union. See Generating the Semantic Value Type, for more details.

See Calc++ Parser and Calc++ Scanner, for a complete example.

- Accepted Values: Any string. Must be a valid identifier prefix in the target language (typically, a possibly empty sequence of letters, underscores, and —not at the beginning— digits).
- Default Value: empty
- History: introduced in Bison 3.0.

Directive: %define api.token.raw
- Language(s): all
Purpose: The output files normally define the enumeration of the token kinds with Yacc-compatible token codes: sequential numbers starting at 257 except for single character tokens which stand for themselves (e.g., in ASCII, ‘'a'’ is numbered 65). The parser however uses symbol kinds which are assigned numbers sequentially starting at 0. Therefore each time the scanner returns an (external) token kind, it must be mapped to the (internal) symbol kind.
When api.token.raw is set, the code of the token kinds are forced to coincide with the symbol kind. This saves one table lookup per token to map them from the token kind to the symbol kind, and also saves the generation of the mapping table. The gain is typically moderate, but in extreme cases (very simple user actions), a 10% improvement can be observed.

When api.token.raw is set, the grammar cannot use character literals (such as ‘'a'’).

- Accepted Values: Boolean.
- Default Value: true in D, false otherwise
- History: introduced in Bison 3.5. Was initially introduced in Bison 1.25 as ‘%raw’, but never worked and was removed in Bison 1.29.

Directive: %define api.value.automove
- Language(s): C++
- Purpose: Let occurrences of semantic values of the right-hand sides of a rule be implicitly turned in rvalues. When enabled, a grammar such as:
```c
exp:
  "number"     { $$ = make_number ($1); }
| exp "+" exp  { $$ = make_binary (add, $1, $3); }
| "(" exp ")"  { $$ = $2; }
```
is actually compiled as if you had written:
```c
exp:
  "number"     { $$ = make_number (std::move ($1)); }
| exp "+" exp  { $$ = make_binary (add,
                                   std::move ($1),
                                   std::move ($3)); }
| "(" exp ")"  { $$ = std::move ($2); }
```
Using a value several times with automove enabled is typically an error. For instance, instead of:
```c
exp: "twice" exp  { $$ = make_binary (add, $2, $2); }
```
write:
```c
exp: "twice" exp { auto v = $2; $$ = make_binary (add, v, v); }
```
It is tempting to use std::move on one of the v, but the argument evaluation order in C++ is unspecified.

- Accepted Values: Boolean.
- Default Value: false
- History: introduced in Bison 3.2

Directive: %define api.value.type support  
Directive: %define api.value.type {type}
- Language(s): all
- Purpose: The type for semantic values.
- Accepted Values:
‘{}’  
This grammar has no semantic value at all. This is not properly supported yet.

‘union-directive’ (C, C++, D)  
The type is defined thanks to the %union directive. You don’t have to define api.value.type in that case, using %union suffices. See The Union Declaration. For instance:
```
%define api.value.type union-directive
%union
{
  int ival;
  char *sval;
}
%token <ival> INT "integer"
%token <sval> STR "string"
```
‘union’ (C, C++)  
The symbols are defined with type names, from which Bison will generate a union. For instance:
```c
%define api.value.type union
%token <int> INT "integer"
%token <char *> STR "string"
```
Most C++ objects cannot be stored in a union, use ‘variant’ instead.

‘variant’ (C++)  
This is similar to union, but special storage techniques are used to allow any kind of C++ object to be used. For instance:
```c
%define api.value.type variant
%token <int> INT "integer"
%token <std::string> STR "string"
See C++ Variants.

‘{type}’
Use this type as semantic value.

%code requires
{
  struct my_value
  {
    enum
    {
      is_int, is_str
    } kind;
    union
    {
      int ival;
      char *sval;
    } u;
  };
}
%define api.value.type {struct my_value}
%token <u.ival> INT "integer"
%token <u.sval> STR "string"
```
- Default Value:  
union-directive if %union is used, otherwise …  
int if type tags are used (i.e., ‘%token <type>…’ or ‘%nterm <type>…’ is used), otherwise …  
undefined.  
- History: introduced in Bison 3.0. Was introduced for Java only in 2.3b as stype.

Directive: %define api.value.union.name name
- Language(s): C
- Purpose: The tag of the generated union (not the name of the typedef). This variable is set to id when ‘%union id’ is used. There is no clear reason to give this union a name.
- Accepted Values: Any valid identifier.
- Default Value: YYSTYPE.
- History: Introduced in Bison 3.0.3.

Directive: %define lr.default-reduction when
- Language(s): all
- Purpose: Specify the kind of states that are permitted to contain default reductions. See Default Reductions.
- Accepted Values: most, consistent, accepting
- Default Value:  
accepting if lr.type is canonical-lr.  
most otherwise.
- History: introduced as lr.default-reductions in 2.5, renamed as lr.default-reduction in 3.0.

Directive: %define lr.keep-unreachable-state
- Language(s): all
- Purpose: Request that Bison allow unreachable parser states to remain in the parser tables. See Unreachable States.
- Accepted Values: Boolean
- Default Value: false
- History: introduced as lr.keep_unreachable_states in 2.3b, renamed as lr.keep-unreachable-states in 2.5, and as lr.keep-unreachable-state in 3.0.

Directive: %define lr.type type
- Language(s): all
- Purpose: Specify the type of parser tables within the LR(1) family. See LR Table Construction.
- Accepted Values: lalr, ielr, canonical-lr
- Default Value: lalr

Directive: %define namespace {namespace}  
Obsoleted by api.namespace

Directive: %define parse.assert
- Languages(s): C, C++
- Purpose: Issue runtime assertions to catch invalid uses. In C, some important invariants in the implementation of the parser are checked when this option is enabled.  
In C++, when variants are used (see C++ Variants), symbols must be constructed and destroyed properly. This option checks these constraints using runtime type information (RTTI). Therefore the generated code cannot be compiled with RTTI disabled (via compiler options such as -fno-rtti).

- Accepted Values: Boolean
- Default Value: false

Directive: %define parse.error verbosity
- Languages(s): all
- Purpose: Control the generation of syntax error messages. See Error Reporting.
- Accepted Values:  
simple Error messages passed to yyerror are simply "syntax error".  
detailed Error messages report the unexpected token, and possibly the expected ones. However, this report can often be incorrect when LAC is not enabled (see LAC). Token name internationalization is supported.  
verbose Similar (but inferior) to detailed. The D parser does not support this value.  
Error messages report the unexpected token, and possibly the expected ones. However, this report can often be incorrect when LAC is not enabled (see LAC).

Does not support token internationalization. Using non-ASCII characters in token aliases is not portable.

custom The user is in charge of generating the syntax error message by defining the yyreport_syntax_error function. See The Syntax Error Reporting Function yyreport_syntax_error.
- Default Value: simple
- History: introduced in 3.0 with support for simple and verbose. Values custom and detailed were introduced in 3.6.

Directive: %define parse.lac when
- Languages(s): C/C++ (deterministic parsers only), D and Java.
- Purpose: Enable LAC (lookahead correction) to improve syntax error handling. See LAC.
- Accepted Values: none, full
- Default Value: none

Directive: %define parse.trace
- Languages(s): C, C++, D, Java
- Purpose: Require parser instrumentation for tracing. See Tracing Your Parser.  
In C/C++, define the macro YYDEBUG (or prefixDEBUG with ‘%define api.prefix {prefix}’), see Multiple Parsers in the Same Program) to 1 (if it is not already defined) so that the debugging facilities are compiled.

- Accepted Values: Boolean
- Default Value: false

Directive: %define parser_class_name {name}  
Obsoleted by api.parser.class


### 3.7.15 %code Summary
The %code directive inserts code verbatim into the output parser source at any of a predefined set of locations. It thus serves as a flexible and user-friendly alternative to the traditional Yacc prologue, %{code%}. This section summarizes the functionality of %code for the various target languages supported by Bison. For a detailed discussion of how to use %code in place of %{code%} for C/C++ and why it is advantageous to do so, see Prologue Alternatives.
```
Directive: %code {code}
```
This is the unqualified form of the %code directive. It inserts code verbatim at a language-dependent default location in the parser implementation.

For C/C++, the default location is the parser implementation file after the usual contents of the parser header file. Thus, the unqualified form replaces %{code%} for most purposes.

For D and Java, the default location is inside the parser class.
```
Directive: %code qualifier {code}
```
This is the qualified form of the %code directive. qualifier identifies the purpose of code and thus the location(s) where Bison should insert it. That is, if you need to specify location-sensitive code that does not belong at the default location selected by the unqualified %code form, use this form instead.

For any particular qualifier or for the unqualified form, if there are multiple occurrences of the %code directive, Bison concatenates the specified code in the order in which it appears in the grammar file.

Not all qualifiers are accepted for all target languages. Unaccepted qualifiers produce an error. Some of the accepted qualifiers are:

requires
- Language(s): C, C++
- Purpose: This is the best place to write dependency code required for the value and location types (YYSTYPE and YYLTYPE in C). In other words, it’s the best place to define types referenced in %union directives. In C, if you use #define to override Bison’s default YYSTYPE and YYLTYPE definitions, then it is also the best place. However you should rather %define api.value.type and api.location.type.  
Location(s): The parser header file and the parser implementation file before the Bison-generated definitions of the value and location types (YYSTYPE and YYLTYPE in C).  

provides
- Language(s): C, C++
- Purpose: This is the best place to write additional definitions and declarations that should be provided to other modules.
- Location(s): The parser header file and the parser implementation file after the Bison-generated value and location types (YYSTYPE and YYLTYPE in C), and token definitions.

top
- Language(s): C, C++
- Purpose: The unqualified %code or %code requires should usually be more appropriate than %code top. However, occasionally it is necessary to insert code much nearer the top of the parser implementation file. For example:
```c
%code top {
  #define _GNU_SOURCE
  #include <stdio.h>
}
```
- Location(s): Near the top of the parser implementation file.

imports
- Language(s): D, Java
- Purpose: This is the best place to write Java import directives. D syntax allows for import statements all throughout the code.
- Location(s): The parser Java file after any Java package directive and before any class definitions. The parser D file before any class definitions.  
Though we say the insertion locations are language-dependent, they are technically skeleton-dependent. Writers of non-standard skeletons however should choose their locations consistently with the behavior of the standard Bison skeletons.

# 4 Parser C-Language Interface
The Bison parser is actually a C function named yyparse. Here we describe the interface conventions of yyparse and the other functions that it needs to use.

Keep in mind that the parser uses many C identifiers starting with ‘yy’ and ‘YY’ for internal purposes. If you use such an identifier (aside from those in this manual) in an action or in epilogue in the grammar file, you are likely to run into trouble.

## 4.1 The Parser Function yyparse
You call the function yyparse to cause parsing to occur. This function reads tokens, executes actions, and ultimately returns when it encounters end-of-input or an unrecoverable syntax error. You can also write an action which directs yyparse to return immediately without reading further.

Function: int yyparse (void)
The value returned by yyparse is 0 if parsing was successful (return is due to end-of-input).

The value is 1 if parsing failed because of invalid input, i.e., input that contains a syntax error or that causes YYABORT to be invoked.

The value is 2 if parsing failed due to memory exhaustion.

In an action, you can cause immediate return from yyparse by using these macros:

Macro: YYACCEPT
Return immediately with value 0 (to report success).

Macro: YYABORT
Return immediately with value 1 (to report failure).

Macro: YYNOMEM
Return immediately with value 2 (to report memory exhaustion).

If you use a reentrant parser, you can optionally pass additional parameter information to it in a reentrant way. To do so, use the declaration %parse-param:

Directive: %parse-param {argument-declaration} …
Declare that one or more argument-declaration are additional yyparse arguments. The argument-declaration is used when declaring functions or prototypes. The last identifier in argument-declaration must be the argument name.

Here’s an example. Write this in the parser:
```c
%parse-param {int *nastiness} {int *randomness}
Then call the parser like this:

{
  int nastiness, randomness;
  …  /* Store proper data in nastiness and randomness. */
  value = yyparse (&nastiness, &randomness);
  …
}
```
In the grammar actions, use expressions like this to refer to the data:
```c
exp: …    { …; *randomness += 1; … }
```
Using the following:
```c
%parse-param {int *randomness}
```
Results in these signatures:
```c
void yyerror (int *randomness, const char *msg);
int  yyparse (int *randomness);
```
Or, if both %define api.pure full (or just %define api.pure) and %locations are used:
```c
void yyerror (YYLTYPE *llocp, int *randomness, const char *msg);
int  yyparse (int *randomness);
```
## 4.5 Special Features for Use in Actions
Here is a table of Bison constructs, variables and macros that are useful in actions.

- Variable: $$  
Acts like a variable that contains the semantic value for the grouping made by the current rule. See Actions.

- Variable: $n  
Acts like a variable that contains the semantic value for the nth component of the current rule. See Actions.

- Variable: $<typealt>$  
Like $$ but specifies alternative typealt in the union specified by the %union declaration. See Data Types of Values in Actions.

- Variable: $<typealt>n  
Like $n but specifies alternative typealt in the union specified by the %union declaration. See Data Types of Values in Actions.

- Macro: YYABORT ;  
Return immediately from yyparse, indicating failure. See The Parser Function yyparse.

- Macro: YYACCEPT ;  
Return immediately from yyparse, indicating success. See The Parser Function yyparse.

- Macro: YYBACKUP (token, value);

Unshift a token. This macro is allowed only for rules that reduce a single value, and only when there is no lookahead token. It is also disallowed in GLR parsers. It installs a lookahead token with token kind token and semantic value value; then it discards the value that was going to be reduced by this rule.

If the macro is used when it is not valid, such as when there is a lookahead token already, then it reports a syntax error with a message ‘cannot back up’ and performs ordinary error recovery.

In either case, the rest of the action is not executed.

- Value: YYEMPTY  
Value stored in yychar when there is no lookahead token.

- Value: YYEOF  
Value stored in yychar when the lookahead is the end of the input stream.

- Macro: YYERROR ;  
Cause an immediate syntax error. This statement initiates error recovery just as if the parser itself had detected an error; however, it does not call yyerror, and does not print any message. If you want to print an error message, call yyerror explicitly before the ‘YYERROR;’ statement. See Error Recovery.

- Macro: YYNOMEM ;  
Return immediately from yyparse, indicating memory exhaustion. See The Parser Function yyparse.

- Macro: YYRECOVERING  
The expression YYRECOVERING () yields 1 when the parser is recovering from a syntax error, and 0 otherwise. See Error Recovery.

- Variable: yychar  
Variable containing either the lookahead token, or YYEOF when the lookahead is the end of the input stream, or YYEMPTY when no lookahead has been performed so the next token is not yet known. Do not modify yychar in a deferred semantic action (see GLR Semantic Actions). See Lookahead Tokens.

- Macro: yyclearin ;  
Discard the current lookahead token. This is useful primarily in error rules. Do not invoke yyclearin in a deferred semantic action (see GLR Semantic Actions). See Error Recovery.

- Macro: yyerrok ;  
Resume generating error messages immediately for subsequent syntax errors. This is useful primarily in error rules. See Error Recovery.

- Variable: yylloc  
Variable containing the lookahead token location when yychar is not set to YYEMPTY or YYEOF. Do not modify yylloc in a deferred semantic action (see GLR Semantic Actions). See Actions and Locations.

- Variable: yylval  
Variable containing the lookahead token semantic value when yychar is not set to YYEMPTY or YYEOF. Do not modify yylval in a deferred semantic action (see GLR Semantic Actions). See Actions.

- Value: @$  
Acts like a structure variable containing information on the textual location of the grouping made by the current rule. See Tracking Locations.

- Value: @n  
Acts like a structure variable containing information on the textual location of the nth component of the current rule. See Tracking Locations.