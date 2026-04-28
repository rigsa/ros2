---
title: "Using Nav2 for Task 3"
---

[Nav2](https://docs.nav2.org/){target="_blank"} is an autonomous navigation stack built into ROS 2. It might seem like the logical choice for Task 3, but there are some important considerations you should make before opting for this approach.

## Some Words of Warning

### “This worked great in simulation, but...”

Many questions we get in the lab start with this phrase.[^a-pound]

[^a-pound]: In fact, if I had £1 for every question I was asked that started like this, I'd be teaching this course remotely from the Bahamas by now :money_mouth:!

Nav2 is a classic example of this: you can spend lots of time carefully crafting a solution that works great in simulation only to find that nothing works the same on the real hardware in the lab. **You will need to do lots of real world testing** to optimise and fine-tune the navigation stack to work effectively in the real robot arena. 

If you want to use Nav2 then make sure you factor this in: you only have limited access to the real hardware, so make sure you plan accordingly and ensure you'll be able to do enough testing to be confident that your solution will work as expected on the day of the assessment. 

Ultimately, **we are unable to give you additional access to the robots outside the labs / drop-in sessions** (and remember that bookings for the drop-ins are limited and available on a first come, first served basis). 

### We Aren’t Nav2 Experts

We (the Robotics Teaching Team) don't have extensive experience in using Nav2 ourselves (we don't have the time!), so if you have problems it's unlikely that we'll be able to help you much in the labs.

### Ensuring Optimal WiFi Performance in the Lab

We are heavily dependent on good WiFi in the lab in order for our robots to work effectively. We've worked very hard to ensure that our robots and our WiFi network in the Diamond are sufficient for *general use* for all teams in the labs (up to 20 robots).[^nics-2026]

[^nics-2026]: In 2026 (for example) we upgraded the WiFI NICs in all of our robots, increasing data throughput by more than 6x. We've also worked extensively with IT Services to optimise the WiFi performance in Diamond Computer Room 5. We are at the point now where we are basically limited by physics!

In the past, we've observed that Nav2 places excessive demand on the network, and results in performance issues for everyone. Ultimately, we don't view Nav2 as a *"general use"* tool, and we therefore will not prioritise this type of usage in the lab. This means, if we observe issues during lab sessions arising due to heavy Nav2 usage, we will place limits on the number of teams who can use it simultaneously. 

## In Summary

Any teams who wish to use Nav2 for Task 3 ***do so at their own risk***.
