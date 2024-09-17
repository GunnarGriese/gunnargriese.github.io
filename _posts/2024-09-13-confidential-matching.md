---
title: Confidential Matching - Smokebomb or Salvation for Advertisers?
author: gunnar
date: 2024-09-19 00:00:01 +0200
categories: [Privacy]
tags: [privacy]
comments: true
---

On September 12, 2024, Google announced a new privacy-focused feature called **Confidential Matching** for their Customer Match tooling in the Google Marketing Platform (GMP) and mentioned applying the same mechanism to Enhanced Conversions. But is this a true breakthrough for privacy-conscious advertisers, or does it obscure deeper concerns? In this blog post, I'll explore Confidential Matching, explain the underlying technical components, how it fits into your digital marketing stack, and critically assess whether this technology is a genuine solution or just another smokescreen in digital advertising. So, let's take it step by step.

## What is Confidential Matching?

As privacy regulations like GDPR and CCPA grow stricter and are adopted more and more over the world, advertisers face increasing challenges when securely using customer data for ad targeting and measurement. Traditionally, tools like Customer Match and Enhanced Conversions required advertisers to share sensitive personal data with Google, raising concerns about data privacy and potential misuse. Confidential Matching offers a solution that allows advertisers to match customer data with Google's records in a way that "preserves privacy". By using Trusted Execution Environments (TEEs), Confidential Matching ensures that data is processed securely without exposing raw information, trying to address privacy concerns while maintaining advertising effectiveness.

## What are Customer Match and Enhanced Conversions?

Customer Match and Enhanced Conversions are two powerful tools in Google's advertising suite that rely on an advertiser's customer data to improve targeting and measurement. Customer Match allows advertisers to upload customer information, such as email addresses or phone numbers, which Google matches with its user base to create highly targeted ad audiences. On the other hand, Enhanced Conversions focuses on accurately attributing ad performance by linking conversions to specific users through shared data. Both tools depend heavily on advertisers providing customer data, which Google uses to match users across its platforms, making data privacy a central concern for businesses.

### Customer Match - Target users that you know

For effective targeted advertising, it is essential to identify subsets of users who are relevant to the business in one way or another. These users might be likely to buy soon, about to churn shortly, or about to exhibit another form of behavior. Businesses often use various data sources to create these segments and identify relevant subsets of users.

![Customer Match](/assets/img/confidential-match/customer-match.png)
_Customer Match - Basic Process_

One of the most valuable data sources is the customer data businesses have collected over time. This data can include email addresses, phone numbers, and behavioral data (e.g., purchase history, website visits and actions). Once advertisers have collected this data and identified relevant subsets of their customers, they can use Customer Match to upload the users' contact information to Google. The upload can be done using manual CSV uploads, the respective APIs, or the Google Ads Data Manager (direct connection to various cloud data storage systems). Google also offers the option to encrypt the data using the SHA256 algorithm before uploading it.

> It is important to note that ever since Google started enforcing its EU consent policy, advertisers need to ensure that they also pass the required consent signals.

Google then compares the uploaded customer data with its user database to find matches and creates a so-called "Customer Match audience" from all the matched entries. The data can also be used to create lookalike audiences, which are users who share characteristics similar to those of the uploaded customer list. The resulting audiences can then be attached to campaigns and ads with messaging directly related to this specific subset of users, which obviously allows for very targeted messaging.

Users who are **signed in to Google services (e.g., Gmail, YouTube)** have given Google permission to use their data for this purpose and match an entry in the uploaded customer list, which will then be exposed to the ads. This allows advertisers to target their existing customers with personalized ads and to reach new users who share similar characteristics with their existing customers.

A pretty powerful tool, don't you agree? Unfortunately, there's a catch. To use this feature, advertisers need to hand over (consented) contact data of their customers to Google and rely on Google not using the data for any (not consented) purposes.

### Enhanced Conversions - Get better insights into your campaign performance

While Customer Match is a tool for delivering targeted advertising messaging, **Enhanced Conversions** is primarily concerned with enhancing the measurement your GMP campaign and ad performance. Both Enhanced Conversions and Customer Match share a common characteristic, though: They rely on the advertiser sharing customer contact data with Google, which Google then matches against its own database entries.

![Enhanced Conversions](/assets/img/confidential-match/enhanced-conversions.png)
_Enhanced Conversions - Basic Process_

In Enhanced Conversions, the customer data is used to more reliably attribute a user's ad exposure or interaction with a conversion registered on the advertiser's website. For Google signed-in users, Google can keep track of all ad impressions and clicks that a specific user had within their ad network. With the advertiser passing on the user's contact details upon a conversion, Google can match its customer data again against the advertiser's customer data.

Matching these deterministic identifiers allows Google to provide the advertiser with accurate reporting on their campaign performance. Google doesn't have to rely on unstable third-party cookies for any matched user. Still, it can use the advertiser's customer data to link ad exposure to business goals. Additionally, better attribution of ad exposure will allow Google's algorithms to optimize the campaigns better, eventually yielding better results for the advertiser.

As you can see, at the end of the day, the mechanism and the associated risks are similar to those of Customer Match. What differs is simply how the data is used within Google's systems.

## Why Confidential Matching?

With the erosion of third-party cookies and other tracking technologies, Google has pushed advertisers to adopt technologies that rely on them sharing more PII with Google. Especially the use of Enhanced Conversions and Customer Match has been promoted as the salvation for advertisers to continue measuring and targeting users across the web. Both technologies require the advertiser to share PII, such as their customers' email addresses and phone numbers, with Google. Google then maps these data points against their user records (e.g., from Google Chrome logged-in users) to improve the measurability of campaign performance and enable retargeting use cases. While the results for businesses that adopted these methods have been nothing short of [impressive](https://www.thinkwithgoogle.com/_qs/documents/14033/final_uk_privacy_playbook.pdf), many businesses have been (rightfully) hesitant to share their customer data with Google due to privacy concerns.

Confidential Matching for Customer Match (and soon for Enhanced Conversions) aims to provide a secure way for advertisers to match their customer data with Google's own data in a "privacy-preserving" manner using Trusted Execution Environments (TEEs). With the introduction of Confidential Matching, Google seeks to address the ever-growing concerns around data privacy and security in digital advertising about Personal Identifiable Information (PII) - in this case, customer data like email addresses, phone numbers, etc.. especially in light of privacy law requirements like the General Data Protection Regulation (GDPR) in Europe and similar laws in the United States, like the California Consumer Privacy Act (CCPA).

Before Confidential Matching, advertisers had to share all their customer data relevant to Customer Match or Enhanced Conversions with Google. Then, Google would use the data it could match within its downstream systems. For the (potentially large) share of unmatched user data, businesses had to trust Google to not further process that data for their own purposes. With Confidential Matching, which operates on TEEs, Google claims to have found a way to match the data without ever seeing the original data itself.

## What are Trusted Execution Environments (TEEs)?

A TEE—also referred to as "Confidential computing"—is an environment for executing code and processing data in a secure and isolated manner. You can think of it like a [clean room](https://digiday.com/marketing/data-clean-room/) where sensitive (or any other) data is processed in a way that the TEE operator (in this case, Google) cannot access. One or multiple data owners send data to the system. The data is encrypted before it enters the TEE and finally decrypted within the TEE.

The TEE ensures that the data is processed securely and that the results are only accessible to authorized parties. Furthermore, the TEE can provide attestation, which is cryptographic proof that the code running in the TEE is genuine and has not been tampered with. At the same time, the TEE is auditable, meaning that the data owner (or a third party) can verify that the data has been processed according to the requirements.

Hence, the core characteristics of TEEs as implemented by Google can be summarized as follows:

1. **Data Isolation**: Google, as the operator of the TEE, cannot access the data processed within the TEE.
2. **Attestation**: The TEE provides cryptographic proof that the code running within it is genuine and has not been tampered with.
3. **Auditable**: The data owner can verify that the data has been processed according to the requirements.

In general, TEEs are an exciting technology for enhancing data privacy and security, as they allow data owners to share their data without exposing each party's actual data.

## Bringing it all together: Confidential Matching

So, how does all of this fit together, and how does it "enhance privacy" (as Google claims)?

There are two main problems with Customer and Enhanced Conversions. The first one is that, in most cases, advertisers share too much data with Google. They'll pass on any customer data and hope that Google finds plenty of matches in their database to enhance their targeting and measurement. The second problem is that once advertisers share the data, they have no control over how Google processes and uses it. Google might use the valuable customer data for their own purposes (other than retargeting or measurement enhancements), for which the advertiser didn't obtain valid user consent.

Now, let's examine how Confidential Matching using TEEs works and whether the issues are addressed adequately.

![Confidential Matching](/assets/img/confidential-match/confidential-match-flow.png)
_Simplified flow diagram of Confidential Matching_

As you can see from the illustration above, both the advertiser and Google upload their customer data to the TEE, where the matching of the two data sources is orchestrated. The output of this matching process is only the data points for which there is a match in Google's database. These matches are then made available in the GMP as audiences or for reporting purposes. Google cannot learn any new data from the advertiser since this is prohibited by the TEE's functionality. In essence, TEEs provide technical guarantees that Google cannot learn new data from advertisers.

## Conclusion

From my perspective (and please keep in mind that I am not a lawyer), Confidential matching seems to solve the issue of excessive data sharing—a data security measure in that sense. What the technology doesn't solve for is the guarantee of purpose limitation, though, once the matched data is in the Google systems.

Now, one might argue that since Google had access to this data all along and (ideally) obtained user consent for their own usage purposes, the advertiser shouldn't be concerned with this. However, assessing this and the general legal compliance of this new approach is beyond my abilities. The future (and people far more intelligent than me) will have to tell if this new approach to sharing PII is a viable approach or just another smoke bomb by Google to eventually circumvent privacy regulations and keep the data kraken alive.

I am happy that Google seems to be investing in technologies that try to balance business needs and user privacy. Regardless, I am not sure that technical solutions alone will be able to solve the underlying issues and concerns of how companies share and handle their customers' data. Hence, my advice if you are considering adopting Confidential Matching is to critically assess its implications on your legal risk profile. For this to be done efficiently, make sure to involve your legal team and conduct a proper risk assessment before adopting this new feature.

I hope you found this article insightful and that you have a better understanding of Confidential Matching. If you have any further questions or need help handling the discussions internally, feel free to contact me via one of the channels listed on this website. Happy tracking!

## References

Links to relevant articles for further reading on the topic:

- [Google announcement](https://blog.google/products/ads-commerce/google-confidential-matching-data-privacy/)
- [Google's GitHub Repo on TEEs](https://github.com/googleads/conf-data-processing-architecture-reference/blob/main/docs/TrustedExecutionEnvironmentsArchitecturalReference.md)
- [Search Engine Land article](https://searchengineland.com/google-confidential-matching-launch-446503)
- [DigiDay article](https://digiday.com/marketing/google-debuts-confidential-matching-a-move-to-quell-advertisers-concerns-around-data-leakage/)
