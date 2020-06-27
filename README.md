```
# Blockchain_Project

🔵 პირველი მოდული - ბლოკჩეინ ტექნოლოგიის მარტივი მაგალითი და API. საკუთარი API-ს სამართავი ბერკეტები.
ამ ნაწილში უკეთესი ვიზუალური კონტაქტის შესაქმნელად და API-ს უფრო მარტივად სამართვად შეგიძლიათ გამოიყენოთ დესკტოპ 
აპლიკაცია: "POSTMAN" 📢📢📢
🌎🌎🌎 https://www.postman.com/downloads/ 🌎🌎🌎

🔵 მეორე მოდული - საკუთარი კრიპტოვალუტის შემქნა და მისი ლოკალურ სერვერზე განთავსება, კრიპტოვალუტის დეცენტრალიზების 
პროცესის სიმულაცია. ეს მოდული საკუთარი კრიპტოვალუტის დემო ვერსიაა. სიმულირების პროცესების აღსაქმელად ჩემი 
რეკომენდაცია იქნება, რომ აუცილებლად გამოიყენოთ, "POSTMAN", დესკტოპ აპლიკაცია. 📢📢📢

🔵 მესამე მოდული მთლიანად დათმობილია რეალური კრიპტოვალუტების მუშაობის პროცესის უკეთ გაანალიზებისთვის საჭირო 
რესურსებზე. ამ ყველაფრის მეტი თვალსაჩინოებისთვის მოდულში მოჩემულია ეგრეთწოდებული ჭკვიანი კონტრაქტი, რომელიც 
დაშენებულია ბლოკჩეინის, კერძოდ - კრიპტოვალუტა/პროტოკოლის ეთერიუმის დემო პროექტების ერთ-ერთ ბაზაზე.
ამ ნაწილში სრულად გამზადებული კოდის გამოყენების საშუალებით ვმუშაობ.

🔵✅ რესურსი გითჰაბზე ✅🔵
🌎🌎🌎 https://github.com/topics/smart-contracts 🌎🌎🌎

🔵✅ SOLIDITY სკრიპტისთვის განკუთვნილი ედიტორი და არა მხოლოდ Solidity. აქ არის გარემო არა მხოლოდ ეთერიუმისთვის 
განკუთვნილი სკრიპტების საწერად არამედ ბიტკოინისთVისაც. ✅🔵
🌎🌎🌎 https://remix.ethereum.org/#optimize=false&evmVersion=null&version=soljson-v0.6.6+commit.6c089d02.js 🌎🌎🌎

აქ კი მოცემულია Solidity სკრიპტი, რომელიც სხვა და სხვა სახის პროცედურას განსაზღვრავს ეთერიუმის მუშაობის 
პრნციპის გამოყენებით და არა მხოლოდ ეთერიუმის.
// Davidcoins ICO 

// Version of Compiler
pragma solidity >=0.4.22 <0.7.0;

contract davidcoin_ico {
    
    // Introducing the maximum number of Davidcoin available for sale 
    uint public max_davidcoins = 1000000;
    
    // Introducing the USD to Davidcoins conversion rate 
    uint public usd_to_davidcoins = 1000;
    
    // Introducing the total number of Davidcoins that have bought by the investors
    uint public total_davidcoins_bought = 0;
    
    // Mapping from the investor address to its equity in Davidcoins and USD 
    mapping(address => uint) equity_davidcoins;
    mapping(address => uint) equity_usd;
    
    // Checking if on investor can buy Davidcoins
    modifier can_buy_davidcoins(uint usd_invested) {
        require (usd_invested * usd_to_davidcoins + total_davidcoins_bought <= max_davidcoins);
        _;
    }
    
    // Getting the equity in Davidcoins of on investor 
    function equity_in_davidcoins(address investor) external constant returns (uint) {
        return equity_davidcoins[investor];
    }
    
    // Getting the equity in USD of an investor
    function equity_in_usd(address investor) external constannt returns (uint) {
        return equity_usd[investor];
    }
    
    // Buying Davidcoins 
    function buy_davidcoins(address investor, uint usd_invested) external 
    can_buy_davidcoins(usd_invested) {
        uint davidcoins_bought = usd_invested * usd_to_davidcoins;
        equity_davidcoins[investor] += davidcoins_bought;
        equity_usd[investor] = equity_davidcoins[investor] / 1000;
        total_davidcoins_bought += davidcoins_bought;
    }
    
    // Selling Davidcoins 
    function sell_davidcoins(address investor, uint davidcoins_sold) external {
        equity_davidcoins[investor] -= davidcoins_sold;
        equity_usd[investor] = equity_davidcoins[investor] / 1000;
        total_davidcoin_bought -= davidcoins_sold;
    }
    
}

```
