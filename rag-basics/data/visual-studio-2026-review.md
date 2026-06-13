# Visual Studio 2026: Smarter, AI, and more modern

May 21, 2026

Today, I woke up and wasn't really feeling like writing code, so I downloaded Visual Studio 2026 and .NET 10.

This is not an article about what Microsoft has introduced in the new versions, but rather a personal opinion based on what I saw and experienced with the latest Visual Studio 2026.

## Visual Studio

The first release of Visual Studio was in 1997, called Visual Studio 97. Between that version and Visual Studio 2026, there were 14 versions.

## The newest version

Visual Studio 2026 has just been released for everyone to download and install. The first release, the Insider's version, was on September 1, 2025.

## Launching

When I launch the Visual Studio 2026 IDE, it starts like version 2022. Select an existing project or create, open (folder), or clone a repository. But the icons are a bit smaller.

The colors are a bit different; the toolbar has a different color (lighter), and overall, it feels a bit more serene, almost calmer.

## Settings in Visual Studio 2026

The settings (or options) in Visual Studio 2026 are a bit different. It's now in a tab, instead of a dialog, which is more consistent with how other parts of Visual Studio work.

But to be honest... It feels a bit chaotic. Like, you have a lot of settings, and they're just thrown into one big heap. I do like the searching and filters at the top of the tab. It makes it easier to find a specific setting.

## AI, AI, AI

The first thing I notice is that Microsoft is heavily promoting AI, particularly Copilot, on its website and in Visual Studio itself. The GitHub Copilot chat is open and focused, which makes it immediately visible. Additionally, the release notes primarily feature AI-based new features.

I am not a big fan of AI. It's a great tool, don't get me wrong! But people are selling it as AI can create whole applications and do everything for us. And I believe this is false. AI (ChatGPT, Copilot, DeepSeek) is a great tool that helps us out when needed. Giving ideas, suggestions, or finding flaws in our code.

## Performance

One of the newer "features" of the new Visual Studio should be performance. Let's test that.

Next, I opened a large solution. A solution that contains 85 C# projects with a mix of different .NET versions. In Visual Studio 2022, loading the entire solution takes around 18 seconds.

Let's do the same in Visual Studio 2026. To load the same solution, it takes 15 seconds — 3 seconds faster. And it's not even loading the Xamarin projects, because they are no longer supported with .NET 10/C# 14 and Visual Studio 2026.

A rebuild (cleaning and building) takes 12 seconds in Visual Studio 2022 and 33 seconds in Visual Studio 2026. Weird. Not sure where this is going wrong.

So, I am not (yet) convinced by Visual Studio 2026 for projects I used to run in Visual Studio 2022. When you create a new project in .NET 9 or 10, you don't get the SLN solution files, but an SLNX (Solution Next) format, which is faster than the normal SLN.

## Benchmarking

One of the new features is the ability to add a benchmark project to your solution. Benchmarking was previously performed using libraries retrieved from NuGet, for example BenchmarkDotNet. You had to install it in Visual Studio, but now it's already included in Visual Studio 2026 as a template.

## Search Text Visualizer

When I work with large files, such as text files or JSON files, it's challenging to pinpoint the information while debugging. But now you can search inside the text visualizer! Open the variable with the Text Visualizer and press Ctrl + F to search for what you need.

## Code Coverage

I was looking at the unit testing features of Visual Studio 2026 and I saw Code Coverage Results! Something that has been consistently missing in the 2022 Community version!

Yes, it's really there! The release notes indicate that it will be available in both the Professional and Community versions. No more need to install extensions to get code coverage in Visual Studio!

## Memory Usage of Visual Studio 2026

It appears that Visual Studio 2026 uses slightly more memory. When I open a project in Visual Studio 2022 (Community), I see it using 555 MB of memory. When I open the same project in Visual Studio 2026, it uses approximately 1.5 GB of memory. Please note that I have some extensions and other software installed in Visual Studio 2022, not in Visual Studio 2026.

Memory could be an issue for Visual Studio 2026, especially on machines with limited RAM.

## Overall Impression

I do like the new look for Visual Studio 2026. Although it's not significantly different from the 2022 version, it does show a slightly calmer design. It's easier to see where you need to be.

The downside is that Microsoft is so focused on AI that it forgets we are developers looking for a way to write code well and fast.

Visual Studio 2026 is slightly faster with an older project, but the difference is not substantial. Newer projects created with .NET 10 load and build faster. However, since many applications are currently built with .NET 8, I doubt many of my clients will upgrade to .NET 10.

The new integrated tools and projects are excellent, as well as the code coverage. It makes Visual Studio 2026 a more complete tool, and it was big already.

The memory is a big downside, if you ask me. Maybe it will improve over time, but having three times more memory for the same project feels a bit unusual.

Visual Studio 2026 shows a lot of potential, and a lot could still change. But I think it could be a worthy successor to Visual Studio 2022.
